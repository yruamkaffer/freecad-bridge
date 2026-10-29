# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Importable conversion engine; host modules are supplied by the entry point."""
import os,json
from mesh_tools import process_mesh
from cad_tools import inventory
import metadata

def consistent(original,candidate):
    if candidate.isNull() or len(candidate.Solids)!=1:return False
    if abs(candidate.Volume-original.Volume)>max(1e-6,abs(original.Volume)*1e-6):return False
    a=original.BoundBox;b=candidate.BoundBox
    return all(abs(getattr(a,k)-getattr(b,k))<1e-5 for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])

def convert_shape(shape,kind,config,MeshPart):
    tolerance=config['tolerance'];best=None;history=[];solid=kind=='solid'
    candidates=[('original',shape)]
    if solid and config.get('repair',True):
        try:
            healed=shape.copy();healed.fix(1e-7,1e-7,1e-5)
            if consistent(shape,healed):candidates.append(('reparo CAD',healed))
            else:history.append('Reparo CAD rejeitado por alteração de volume ou dimensões.')
        except Exception as error:history.append('Reparo CAD indisponível: '+str(error))
    for label,candidate in candidates:
        attempts=[('MeshPart',tolerance,0.15)]
        if config.get('repair',True):attempts += [('MeshPart',tolerance,0.08),('MeshPart',tolerance*.5,0.08),('tessellate',tolerance,0)]
        for method,linear,angular in attempts:
            try:
                fresh=candidate.copy()
                if method=='MeshPart':
                    mesh=MeshPart.meshFromShape(Shape=fresh,LinearDeflection=linear,AngularDeflection=angular,Relative=False)
                    points,facets=mesh.Topology
                else:points,facets=fresh.tessellate(linear)
                mesh=process_mesh([[p.x,p.y,p.z] for p in points],facets,config.get('mesh_treatment','complete'),is_solid=solid)
                check=mesh['check'];valid=bool(candidate.isValid())
                history.extend(mesh['repair_attempts'])
                result=dict(vertices=mesh['vertices'],triangles=mesh['triangles'],mesh_closed=check['closed'],
                            cad_valid=valid if solid else False,cad_shape_valid=valid,cad_has_solid=solid,
                            geometry_type=kind,conversion=label+' / '+method,linear_deflection=linear,
                            check=check,repairs=mesh['repairs'],repair_attempts=mesh['repair_attempts'],
                            _color_geometry=mesh['color_geometry'],_triangle_sources=mesh['triangle_sources'])
                history.append('%s/%s: %d abertas, %d não-manifold, %d conflitos, %d vértices problemáticos' %
                               (label,method,check['boundary'],check['nonmanifold'],check['conflicts'],check['nonmanifold_vertices']))
                score=(not check['closed'],not valid,check['nonmanifold'],check['boundary'],check['conflicts'],check['nonmanifold_vertices'],check['degenerate'])
                if best is None or score<best[0]:best=(score,result)
                if not solid or (check['closed'] and valid):return result,history
            except Exception as error:history.append(label+'/'+method+': '+str(error))
    if best is None:raise RuntimeError('Nenhuma triangulação produzida. '+'; '.join(history))
    return best[1],history

def apply_colors(result,original,record,tolerance):
    baseline=result['_color_geometry']
    metadata.transfer_colors(baseline,original,record,tolerance)
    if 'color' in baseline:result['color']=baseline['color'];return 0
    if 'triangle_colors' in baseline:
        colors=baseline['triangle_colors'];result['triangle_colors']=[colors[i] for i in result['_triangle_sources']]
        return sum(c is None for c in result['triangle_colors'])
    return len(result['triangles'])

def run(config,App,Part,MeshPart):
    policy=config.get('policy','visualization' if config.get('allow_open',False) else 'strict')
    if policy not in ('strict','visualization','solids_only'):raise ValueError('Modo inválido.')
    if not 0.001<=float(config['tolerance'])<=100:raise ValueError('Desvio fora do intervalo 0,001–100 mm.')
    if config.get('input_type')=='json':return run_json(config)
    shape=Part.read(config['source']);parts=[];warnings=[];skipped=[];failures=[]
    metadata_doc=None;records=[]
    try:
        try:metadata_doc,records=metadata.read(config['source'],App)
        except Exception as error:warnings.append('Nomes/cores não puderam ser lidos: '+str(error))
        items=inventory(shape)
        if not items:raise RuntimeError('STEP sem sólidos ou superfícies; entidades somente de linha não são importadas.')
        for number,(kind,item) in enumerate(items,1):
            try:record=metadata.choose(item,records,kind)
            except Exception as error:
                record=None;warnings.append('Peça_%02d: associação de metadados indisponível: %s'%(number,error))
            name=record['name'] if record else ('Peça_%02d'%number)
            if kind=='surface' and policy!='visualization':
                message=name+': superfície/casca fora de um sólido; não foi fechada automaticamente.'
                skipped.append(dict(source_index=number,name=name,geometry_type=kind,reason=message))
                if policy=='strict':failures.append(message)
                continue
            try:result,history=convert_shape(item,kind,config,MeshPart)
            except Exception as error:
                message=name+': '+str(error)
                if policy=='solids_only':skipped.append(dict(source_index=number,name=name,geometry_type=kind,reason=message));continue
                failures.append(message);continue
            result.update(name=name,source_index=number)
            if record:
                try:
                    missing=apply_colors(result,item,record,result['linear_deflection'])
                    if missing:warnings.append(name+': %d triângulos sem cor confirmada.'%missing)
                except Exception as error:warnings.append(name+': cores não transferidas: '+str(error))
            else:warnings.append(name+': nome/cor não associados com segurança.')
            result.pop('_color_geometry',None);result.pop('_triangle_sources',None)
            approved=kind=='solid' and result['mesh_closed'] and result['cad_valid']
            if not approved:
                message=name+(': superfície/casca importada para inspeção.' if kind=='surface' else ': reparo não resolveu. '+'; '.join(history))
                if policy=='strict':failures.append(message);continue
                if policy=='solids_only':skipped.append(dict(source_index=number,name=name,geometry_type=kind,reason=message));continue
                warnings.append(message)
            result['conversion_history']=history
            parts.append(result)
        if failures:raise RuntimeError('Importação não concluída:\n'+'\n'.join(failures)+'\nUse Visualização para inspecionar as peças ou Sólidos disponíveis para omitir explicitamente as não aprovadas.')
        if not parts:raise RuntimeError('Nenhuma peça aprovada no modo escolhido. '+'; '.join(p['reason'] for p in skipped))
        warnings += ['OMITIDA — '+p['reason'] for p in skipped]
        return dict(format='yk-step-bridge-1',units='mm',source=os.path.basename(config['source']),parts=parts,
                    warnings=warnings,strict=policy!='visualization',policy=policy,skipped_parts=skipped,
                    mesh_treatment=config.get('mesh_treatment','complete'),generator_version='0.5.0')
    finally:
        if metadata_doc is not None:App.closeDocument(metadata_doc.Name)

def run_json(config):
    """Explicit reprocessing preserves material provenance without re-reading CAD."""
    with open(config['source'],encoding='utf-8') as f:data=json.load(f)
    if data.get('format')!='yk-step-bridge-1' or data.get('units')!='mm':raise ValueError('JSON incompatível.')
    policy=config.get('policy','strict');parts=[];skipped=[dict(p,origin='source_json') for p in data.get('skipped_parts',[])];failures=[]
    if policy not in ('strict','visualization','solids_only'):raise ValueError('Modo inválido.')
    warnings=list(data.get('warnings',[]))+['JSON reprocessado: validade CAD não foi reavaliada; geometria de origem é a do JSON.']
    for i,original in enumerate(data.get('parts',[]),1):
        name=original.get('name','Peça_%02d'%i)
        kind='surface' if original.get('geometry_type')=='surface' or original.get('cad_has_solid') is False else 'solid'
        if kind=='surface' and policy!='visualization':
            message=name+': superfície não aprovada para o modo escolhido.'
            skipped.append(dict(source_index=original.get('source_index',i),name=name,geometry_type=kind,reason=message))
            if policy=='strict':failures.append(message)
            continue
        colors=original.get('triangle_colors')
        if colors is not None and len(colors)!=len(original['triangles']):raise ValueError(name+': quantidade de cores incompatível.')
        mesh=process_mesh(original['vertices'],original['triangles'],config.get('mesh_treatment','complete'),is_solid=kind=='solid')
        p=dict(original);p.update(name=name,geometry_type=kind,vertices=mesh['vertices'],triangles=mesh['triangles'],
                                mesh_closed=mesh['check']['closed'],check=mesh['check'],source_index=original.get('source_index',i),
                                repairs=list(original.get('repairs',[]))+mesh['repairs'],repair_attempts=mesh['repair_attempts'])
        if colors is not None:p['triangle_colors']=[colors[j] for j in mesh['input_triangle_sources']]
        approved=kind=='solid' and p['mesh_closed'] and p.get('cad_valid') is not False
        if not approved and policy!='visualization':
            message=name+': geometria não aprovada após tratamento.'
            if policy=='strict':failures.append(message)
            else:skipped.append(dict(source_index=p['source_index'],name=name,geometry_type=kind,reason=message))
            continue
        parts.append(p)
    if failures:raise RuntimeError('\n'.join(failures)+'\nUse Visualização para inspecionar ou Sólidos disponíveis para omitir as peças não aprovadas.')
    if not parts:raise RuntimeError('Nenhuma peça aprovada no JSON para o modo escolhido.')
    warnings+=['OMITIDA — '+p['reason'] for p in skipped]
    return dict(format='yk-step-bridge-1',units='mm',source=data.get('source',os.path.basename(config['source'])),
                parts=parts,warnings=warnings,strict=policy!='visualization',policy=policy,skipped_parts=skipped,
                mesh_treatment=config.get('mesh_treatment','complete'),generator_version='0.5.0')
