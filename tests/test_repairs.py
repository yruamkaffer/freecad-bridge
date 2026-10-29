# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import json,sys,tempfile,unittest,types
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'yk_step_bridge'))
from mesh_tools import process_mesh,prepare,audit,signed_volume
from conversion import run,run_json,apply_colors
from cad_tools import inventory

def thin_tetra():
    return [[0,0,0],[10,0,0],[0,10,0],[0,0,10],[.00001,0,0]],[[0,2,4],[4,2,1],[0,4,3],[4,1,3],[0,3,2],[1,2,3]]
def touching_tetra():
    v=[[0,0,0],[100,0,0],[0,100,0],[0,0,100],[0,-100,0],[0,0,-100]]
    t=[[0,2,1],[0,1,3],[0,3,2],[1,2,3],[0,4,1],[0,1,5],[0,5,4],[1,4,5]]
    return v,t
class Shape:
    def __init__(self,token,solids=(),shells=(),faces=()):self.token,self.Solids,self.Shells,self.Faces=token,list(solids),list(shells),list(faces)
    def isSame(self,other):return self.token==other.token
class RepairTests(unittest.TestCase):
    def test_weld_removes_sliver_and_preserves_volume(self):
        v,t=thin_tetra();r=process_mesh(v,t,'conservative')
        self.assertTrue(r['check']['closed']);self.assertEqual(len(r['triangles']),4)
        self.assertEqual(r['repairs'][0]['operation'],'merge_near_vertices')
        self.assertAlmostEqual(abs(signed_volume(r['vertices'],r['triangles'])),1000/6)
        self.assertEqual(len(r['triangle_sources']),4)
    def test_none_leaves_sliver_available_for_diagnosis(self):
        v,t=thin_tetra();r=process_mesh(v,t,'none')
        self.assertEqual(r['repairs'],[]);self.assertEqual(len(r['triangles']),6)
        self.assertGreater(r['check']['thin_triangles'],0)
    def test_complete_separates_touching_closed_surfaces(self):
        v,t=touching_tetra();before=process_mesh(v,t,'conservative');r=process_mesh(v,t,'complete')
        self.assertFalse(before['check']['closed']);self.assertGreater(before['check']['nonmanifold'],0)
        self.assertTrue(r['check']['closed']);self.assertEqual(r['check']['nonmanifold_vertices'],0)
        self.assertEqual(r['check']['components'],2);self.assertEqual(len(r['triangles']),len(t))
        self.assertEqual(r['repairs'][0]['max_displacement_mm'],.001)
        self.assertLess(r['repairs'][0]['relative_volume_change'],1e-4)
    def test_small_contact_rejected_when_volume_change_is_excessive(self):
        v,t=touching_tetra();v=[[x*.00001 for x in p] for p in v]
        r=process_mesh(v,t,'complete');self.assertFalse(r['check']['closed']);self.assertEqual(r['repairs'],[])
        self.assertTrue(r['repair_attempts'])
    def test_open_surface_is_not_capped(self):
        r=process_mesh([[0,0,0],[10,0,0],[0,10,0]],[[0,1,2]],'complete',is_solid=False)
        self.assertFalse(r['check']['closed']);self.assertEqual(r['check']['boundary'],3)
        self.assertEqual(r['repairs'],[]);self.assertEqual(len(r['triangles']),1)
    def test_pinched_vertex_rejected_even_with_two_faces_per_edge(self):
        v,t=touching_tetra();v=v+[[100,100,100],[100,0,100],[100,100,0]]
        # Separate tetra sharing just vertex 1, not an edge.
        t=t[:4]+[[1,6,7],[1,8,6],[1,7,8],[6,8,7]]
        _,_,c=prepare(v,t);self.assertEqual(c['nonmanifold'],0);self.assertFalse(c['closed'])
        self.assertGreater(c['nonmanifold_vertices'],0)
    def test_invalid_coordinates_rejected(self):
        with self.assertRaises(ValueError):prepare([[float('nan'),0,0]],[])
        with self.assertRaises(ValueError):prepare([[0,0,0]],[[0,1,2]])
    def test_inventory_keeps_loose_shell_and_face_without_duplicating_solid_faces(self):
        f1,f2,f3=[Shape(x) for x in ('solid_face','surface_face','loose_face')]
        s1=Shape('solid_shell',faces=[f1]);s2=Shape('surface_shell',faces=[f2]);solid=Shape('solid',shells=[s1],faces=[f1])
        whole=Shape('all',solids=[solid],shells=[s1,s2],faces=[f1,f2,f3])
        result=inventory(whole);self.assertEqual([(k,s.token) for k,s in result],[('solid','solid'),('surface','surface_shell'),('surface','loose_face')])
    def test_color_provenance_survives_weld(self):
        v,t=thin_tetra();colors=[[i*30,0,0] for i in range(len(t))]
        d=dict(format='yk-step-bridge-1',units='mm',source='synthetic',parts=[dict(name='thin',vertices=v,triangles=t,cad_valid=True,triangle_colors=colors)])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'mesh.json';path.write_text(json.dumps(d));r=run_json(dict(source=str(path),policy='strict',mesh_treatment='complete'))
        p=r['parts'][0];self.assertTrue(p['mesh_closed']);self.assertEqual(len(p['triangle_colors']),4)
        # Small faces 0 and 2 collapsed; surviving original triangle colors follow provenance.
        self.assertEqual(p['triangle_colors'],[colors[i] for i in [1,3,4,5]])
    def test_conversion_colors_use_original_mesh_before_vertex_displacement(self):
        baseline={'vertices':[[0,0,0]],'triangles':[[0,0,0]]};result={'_color_geometry':baseline,'_triangle_sources':[1,0]}
        def transfer(mesh,*args):
            self.assertIs(mesh,baseline);mesh['triangle_colors']=[[255,0,0],[0,0,255]]
        with patch('metadata.transfer_colors',side_effect=transfer):self.assertEqual(apply_colors(result,None,{},.05),0)
        self.assertEqual(result['triangle_colors'],[[0,0,255],[255,0,0]])
    def test_json_modes_never_silently_discard_surface(self):
        v,t=thin_tetra();surface=dict(name='support',vertices=[[0,0,0],[1,0,0],[0,1,0]],triangles=[[0,1,2]],cad_has_solid=False,cad_valid=False,geometry_type='surface')
        d=dict(format='yk-step-bridge-1',units='mm',parts=[dict(name='solid',vertices=v,triangles=t,cad_valid=True),surface])
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'mesh.json';p.write_text(json.dumps(d));c=dict(source=str(p),mesh_treatment='complete')
            with self.assertRaisesRegex(RuntimeError,'support'):run_json(dict(c,policy='strict'))
            visual=run_json(dict(c,policy='visualization'));self.assertEqual(len(visual['parts']),2);self.assertFalse(visual['strict'])
            partial=run_json(dict(c,policy='solids_only'));self.assertEqual(len(partial['parts']),1)
            self.assertEqual(partial['skipped_parts'][0]['name'],'support');self.assertTrue(partial['strict'])
    def test_step_policies_keep_surface_and_omissions_explicit(self):
        solid,surface=object(),object()
        def convert(item,kind,*args):
            v,t=thin_tetra();m=process_mesh(v,t)
            p=dict(vertices=m['vertices'],triangles=m['triangles'],check=m['check'],mesh_closed=kind=='solid',
                   cad_valid=kind=='solid',cad_has_solid=kind=='solid',geometry_type=kind,repairs=[],repair_attempts=[],
                   linear_deflection=.05,_color_geometry=m['color_geometry'],_triangle_sources=m['triangle_sources'])
            return p,[]
        for policy in ['strict','visualization','solids_only']:
            app=types.SimpleNamespace(closeDocument=unittest.mock.Mock())
            part=types.SimpleNamespace(read=lambda path:None)
            with patch('conversion.inventory',return_value=[('solid',solid),('surface',surface)]), patch('metadata.read',return_value=(types.SimpleNamespace(Name='test_doc'),[])), patch('metadata.choose',side_effect=lambda item,*a:{'name':'support' if item is surface else 'solid'}), patch('conversion.apply_colors',return_value=0), patch('conversion.convert_shape',side_effect=convert):
                config=dict(source='test.step',tolerance=.05,policy=policy)
                if policy=='strict':
                    with self.assertRaisesRegex(RuntimeError,'support'):run(config,app,part,None)
                else:
                    result=run(config,app,part,None)
                    self.assertEqual(len(result['parts']),2 if policy=='visualization' else 1)
                    self.assertEqual(len(result['skipped_parts']),0 if policy=='visualization' else 1)
                app.closeDocument.assert_called_once_with('test_doc')
    def test_json_reprocessing_retains_preexisting_omissions(self):
        v,t=thin_tetra();d=dict(format='yk-step-bridge-1',units='mm',parts=[dict(name='solid',vertices=v,triangles=t)],skipped_parts=[dict(name='support',source_index=2,reason='open surface')])
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'mesh.json';p.write_text(json.dumps(d));result=run_json(dict(source=str(p)))
        self.assertEqual(result['skipped_parts'][0]['name'],'support')
        self.assertEqual(result['skipped_parts'][0]['origin'],'source_json')
    def test_empty_json_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'empty.json';p.write_text(json.dumps(dict(format='yk-step-bridge-1',units='mm',parts=[])))
            with self.assertRaisesRegex(RuntimeError,'Nenhuma'):run_json(dict(source=str(p)))
if __name__=='__main__':unittest.main()
