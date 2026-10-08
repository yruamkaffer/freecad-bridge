# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os,sys,json,traceback
import FreeCAD as App
import Part,MeshPart
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mesh_tools import prepare
import metadata
config=json.load(open(os.environ['YK_STEP_JOB'],encoding='utf-8'));output=config['output']

def consistent(original,candidate):
    if candidate.isNull() or len(candidate.Solids)!=1:return False
    # Healing must not noticeably change volume or placement.
    if abs(candidate.Volume-original.Volume)>max(1e-6,abs(original.Volume)*1e-6):return False
    a=original.BoundBox;b=candidate.BoundBox
    return all(abs(getattr(a,k)-getattr(b,k))<1e-5 for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])

def convert(solid):
    tolerance=config['tolerance']; best=None; history=[]
    candidates=[('original',solid)]
    if config.get('repair',True):
        try:
            healed=solid.copy();healed.fix(1e-7,1e-7,1e-5)
            if consistent(solid,healed):candidates.append(('reparo CAD',healed))
            else:history.append('Reparo CAD rejeitado por alteração de volume ou dimensões.')
        except Exception as error:history.append('Reparo CAD indisponível: '+str(error))
    for label,candidate in candidates:
        attempts=[('MeshPart',tolerance,0.15)]
        if config.get('repair',True):
            attempts += [('MeshPart',tolerance,0.08),('MeshPart',tolerance*0.5,0.08),('tessellate',tolerance,0)]
        for method,linear,angular in attempts:
            try:
                fresh=candidate.copy()
                if method=='MeshPart':
                    mesh=MeshPart.meshFromShape(Shape=fresh,LinearDeflection=linear,AngularDeflection=angular,Relative=False)
                    points,facets=mesh.Topology
                else:points,facets=fresh.tessellate(linear)
                vertices,triangles,check=prepare([[p.x,p.y,p.z] for p in points],facets)
                result={'vertices':vertices,'triangles':triangles,'mesh_closed':check['closed'],'cad_valid':candidate.isValid(),'conversion':label+' / '+method,'linear_deflection':linear,'check':check}
                history.append('%s/%s: %d abertas, %d não-manifold, %d conflitos' % (label,method,check['boundary'],check['nonmanifold'],check['conflicts']))
                score=(not check['closed'],not candidate.isValid(),check['nonmanifold'],check['boundary'],check['conflicts'])
                if best is None or score<best[0]:best=(score,result)
                if check['closed'] and candidate.isValid():return result,history
            except Exception as error:history.append(label+'/'+method+': '+str(error))
    if best is None:raise RuntimeError('Nenhuma triangulação produzida. '+ '; '.join(history))
    return best[1],history

try:
    shape=Part.read(config['source']);parts=[];warnings=[]
    metadata_doc=None;records=[]
    try:metadata_doc,records=metadata.read(config['source'],App)
    except Exception as error:warnings.append('Nomes/cores não puderam ser lidos: '+str(error))
    for number,solid in enumerate(shape.Solids):
        result,history=convert(solid);result['name']='Peça_%02d' % (number+1)
        result['source_index']=number+1
        record=metadata.choose(solid,records)
        if record:
            result['name']=record['name']
            try:
                missing=metadata.transfer_colors(result,solid,record,result.get('linear_deflection',config['tolerance']))
                if missing:warnings.append(result['name']+': %d triângulos sem cor confirmada.' % missing)
            except Exception as error:warnings.append(result['name']+': cores não transferidas: '+str(error))
        else:warnings.append(result['name']+': nome/cor não associados com segurança.')
        if not result['mesh_closed'] or not result['cad_valid']:
            message=result['name']+': reparo não resolveu. '+ '; '.join(history)
            if not config.get('allow_open',False):raise RuntimeError(message+' Use Visualização para importar com avisos.')
            warnings.append(message)
        elif result['conversion']!='original / MeshPart':warnings.append(result['name']+': recuperada por '+result['conversion'])
        parts.append(result)
    if not parts:raise RuntimeError('STEP sem sólidos.')
    with open(output+'.tmp','w',encoding='utf-8') as f:json.dump({'format':'yk-step-bridge-1','units':'mm','source':os.path.basename(config['source']),'parts':parts,'warnings':warnings,'strict':not config.get('allow_open',False)},f,ensure_ascii=False)
    os.replace(output+'.tmp',output)
except Exception:
    with open(output+'.error','w',encoding='utf-8') as f:f.write(traceback.format_exc())
os._exit(0 if os.path.isfile(output) else 1)
