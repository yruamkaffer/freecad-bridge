# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Offline regression checks; no host application APIs loaded."""
from pathlib import Path
import sys,types,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'yk_step_bridge'))
import metadata
from mesh_tools import prepare
class Point:
 def __init__(self,x,y,z):self.x,self.y,self.z=x,y,z
class Face:
 def tessellate(self,tolerance):return [Point(0,0,0),Point(1,0,0),Point(0,1,0)],[(0,1,2)]
class CoreTests(unittest.TestCase):
 def test_invalid_and_normalized_colors(self):
  self.assertEqual(metadata.rgb((1,.5,0)),[255,128,0])
  for value in [(float('nan'),0,0),(2,0,0),(-1,0,0),None,(1,)]:self.assertIsNone(metadata.rgb(value))
 def test_ambiguous_metadata_not_associated(self):
  shape=types.SimpleNamespace(Volume=10,BoundBox=types.SimpleNamespace(XMin=0,XMax=1,YMin=0,YMax=1,ZMin=0,ZMax=1),CenterOfMass=Point(.5,.5,.5))
  record={'signature':metadata.signature(shape)}
  self.assertIs(metadata.choose(shape,[record]),record)
  self.assertIsNone(metadata.choose(shape,[record,dict(record)]))
  self.assertIsNone(metadata.choose(shape,[]))
 def test_color_mapping_ignores_orientation(self):
  result={'vertices':[[0,0,0],[1,0,0],[0,1,0]],'triangles':[[2,1,0]]}
  record={'color':None,'face_colors':[[255,0,0]],'shape':types.SimpleNamespace(Faces=[Face()])}
  self.assertEqual(metadata.transfer_colors(result,None,record,.05),0)
  self.assertEqual(result['triangle_colors'],[[255,0,0]])
 def test_unmatched_triangle_unpainted(self):
  result={'vertices':[[0,0,1],[1,0,1],[0,1,1]],'triangles':[[0,1,2]]}
  record={'color':None,'face_colors':[[255,0,0]],'shape':types.SimpleNamespace(Faces=[Face()])}
  self.assertEqual(metadata.transfer_colors(result,None,record,.05),1)
  self.assertEqual(result['triangle_colors'],[None])
 def test_closed_tetrahedron_duplicate_reversed_face(self):
  points=[[0,0,0],[10,0,0],[0,10,0],[0,0,10]]
  _,triangles,check=prepare(points,[[0,2,1],[0,1,3],[0,3,2],[3,2,1],[1,2,0]])
  self.assertTrue(check['closed']);self.assertEqual(len(triangles),4)
 def test_open_tetrahedron_rejected(self):
  _,_,check=prepare([[0,0,0],[10,0,0],[0,10,0],[0,0,10]],[[0,2,1],[0,1,3],[0,3,2]])
  self.assertFalse(check['closed']);self.assertEqual(check['boundary'],3)
if __name__=='__main__':unittest.main()
