# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Mesh checks and bounded repairs. Millimetres; Python standard library only."""
from collections import defaultdict, deque
from itertools import product
import math

WELD_MM = 0.0001
SEPARATION_MM = 0.001
THIN_HEIGHT_MM = 0.0000254  # Small-face risk at the importer's 1000x construction scale.

def sub(a,b):return [a[k]-b[k] for k in range(3)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):return math.sqrt(dot(a,a))
def normal(vertices,t):return cross(sub(vertices[t[1]],vertices[t[0]]),sub(vertices[t[2]],vertices[t[0]]))

def edges_of(triangles):
    edges=defaultdict(list)
    for i,t in enumerate(triangles):
        for a,b in zip(t,t[1:]+t[:1]):edges[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
    return edges

def signed_volume(vertices,triangles):
    if not vertices:return 0.0
    origin=vertices[0]
    return math.fsum(dot(sub(vertices[t[0]],origin),cross(sub(vertices[t[1]],origin),sub(vertices[t[2]],origin))) for t in triangles)/6.0

def audit(vertices,triangles):
    edges=edges_of(triangles);links=defaultdict(list);incident=defaultdict(set);graph=defaultdict(set)
    for i,t in enumerate(triangles):
        for v in t:incident[v].add(i)
    boundary=sum(len(v)==1 for v in edges.values());nonmanifold=sum(len(v)>2 for v in edges.values())
    conflicts=sum(len(v)==2 and v[0][1]==v[1][1] for v in edges.values())
    for (a,b),pair in edges.items():
        if len(pair)!=2:continue
        i,j=pair[0][0],pair[1][0]
        links[a].append((i,j));links[b].append((i,j));graph[i].add(j);graph[j].add(i)
    bad_vertices=0
    for v,faces in incident.items():
        local=defaultdict(list)
        for i,j in links[v]:local[i].append(j);local[j].append(i)
        start=next(iter(faces));seen={start};queue=[start]
        while queue:
            for j in local[queue.pop()]:
                if j not in seen:seen.add(j);queue.append(j)
        if seen!=faces:bad_vertices+=1
    seen=set();components=0
    for i in range(len(triangles)):
        if i in seen:continue
        components+=1;seen.add(i);queue=[i]
        while queue:
            for j in graph[queue.pop()]:
                if j not in seen:seen.add(j);queue.append(j)
    thin=zero=0;min_height=None
    for t in triangles:
        height=norm(normal(vertices,t))/max([norm(sub(vertices[a],vertices[b])) for a,b in zip(t,t[1:]+t[:1])]+[1e-30])
        if height<=1e-12:zero+=1
        if height<THIN_HEIGHT_MM:thin+=1
        min_height=height if min_height is None else min(min_height,height)
    closed=bool(triangles) and not any([boundary,nonmanifold,conflicts,bad_vertices,zero])
    return dict(closed=closed,boundary=boundary,nonmanifold=nonmanifold,conflicts=conflicts,
                nonmanifold_vertices=bad_vertices,degenerate=zero,thin_triangles=thin,
                min_height_mm=min_height,components=components)

def _normalize(points,facets):
    vertices=[];mapping=[];lookup={}
    for p in points:
        xyz=[float(p[0]),float(p[1]),float(p[2])]
        if not all(math.isfinite(x) for x in xyz):raise ValueError('Coordenada não finita.')
        key=tuple(round(x,8) for x in xyz)
        if key not in lookup:lookup[key]=len(vertices);vertices.append(xyz)
        mapping.append(lookup[key])
    triangles=[];sources=[];seen=set()
    for i,facet in enumerate(facets):
        if len(facet)!=3 or any(not isinstance(k,int) or k<0 or k>=len(mapping) for k in facet):raise ValueError('Triângulo inválido.')
        t=[mapping[k] for k in facet];key=tuple(sorted(t))
        if len(set(t))<3 or key in seen:continue
        seen.add(key);triangles.append(t);sources.append(i)
    edges=edges_of(triangles);graph=defaultdict(list)
    for pair in edges.values():
        if len(pair)==2:
            (i,di),(j,dj)=pair;graph[i].append((j,-di*dj));graph[j].append((i,-di*dj))
    orientation={}
    for start in range(len(triangles)):
        if start in orientation:continue
        orientation[start]=1;queue=deque([start])
        while queue:
            i=queue.popleft()
            for j,rel in graph[i]:
                if j not in orientation:orientation[j]=orientation[i]*rel;queue.append(j)
    for i,direction in orientation.items():
        if direction<0:triangles[i].reverse()
    if signed_volume(vertices,triangles)<0:
        for t in triangles:t.reverse()
    return vertices,triangles,sources

def prepare(points,facets):
    vertices,triangles,_=_normalize(points,facets)
    return vertices,triangles,audit(vertices,triangles)

def _accepted(oldv,oldt,newv,newt,sources,max_move,max_relative_volume,oldcheck):
    check=audit(newv,newt)
    if not check['closed']:return None,'malha candidata não fechou ou tem degenerações'
    if check['components']!=oldcheck['components']:return None,'quantidade de regiões conectadas mudou'
    if check['thin_triangles']>oldcheck['thin_triangles']:return None,'novos triângulos muito estreitos'
    for t,i in zip(newt,sources):
        if dot(normal(oldv,oldt[i]),normal(newv,t))<=0:return None,'face invertida ou degenerada'
    before=signed_volume(oldv,oldt);after=signed_volume(newv,newt)
    if abs(before)<1e-12:return None,'volume de referência insuficiente'
    relative=abs(after-before)/abs(before)
    if relative>max_relative_volume:return None,'variação de volume excedeu limite'
    for k in range(3):
        if abs(min(p[k] for p in oldv)-min(p[k] for p in newv))>max_move+1e-9:return None,'limite dimensional excedido'
        if abs(max(p[k] for p in oldv)-max(p[k] for p in newv))>max_move+1e-9:return None,'limite dimensional excedido'
    return dict(check=check,volume_before_mm3=before,volume_after_mm3=after,relative_volume_change=relative),None

def _weld(vertices,triangles,check):
    bins=defaultdict(list);out=[];mapping=[];changed=0
    for p in vertices:
        key=tuple(math.floor(x/WELD_MM) for x in p);found=None
        for delta in product((-1,0,1),repeat=3):
            for j in bins[tuple(a+b for a,b in zip(key,delta))]:
                if norm(sub(p,out[j]))<=WELD_MM:found=j;break
            if found is not None:break
        if found is None:found=len(out);out.append(list(p));bins[key].append(found)
        else:changed+=1
        mapping.append(found)
    if not changed:return None,'nenhum par dentro da tolerância'
    tris=[];sources=[];seen=set()
    for i,t in enumerate(triangles):
        t=[mapping[v] for v in t];key=tuple(sorted(t))
        if len(set(t))<3 or key in seen:continue
        seen.add(key);tris.append(t);sources.append(i)
    accepted,reason=_accepted(vertices,triangles,out,tris,sources,WELD_MM,1e-6,check)
    if accepted is None:return None,reason
    info=dict(operation='merge_near_vertices',tolerance_mm=WELD_MM,merged_vertices=changed,
              removed_triangles=len(triangles)-len(tris),**accepted)
    return (out,tris,sources,info),None

def _separate(vertices,triangles,check):
    edges=edges_of(triangles);bad={v for edge,pair in edges.items() if len(pair)>2 for v in edge}
    if not bad:return None,'nenhuma aresta de contato'
    if len(bad)>512:return None,'mais de 512 vértices problemáticos; exige revisão'
    incident=defaultdict(list);local_edges=defaultdict(list)
    for i,t in enumerate(triangles):
        for v in t:
            if v in bad:incident[v].append(i)
    for edge,pair in edges.items():
        for v in edge:
            if v in bad and len(pair)==2:local_edges[v].append((pair[0][0],pair[1][0]))
    out=[list(p) for p in vertices];tris=[list(t) for t in triangles]
    for v in sorted(bad):
        graph=defaultdict(list)
        for i,j in local_edges[v]:graph[i].append(j);graph[j].append(i)
        seen=set();fans=[]
        for start in incident[v]:
            if start in seen:continue
            seen.add(start);queue=[start];fan=[]
            while queue:
                i=queue.pop();fan.append(i)
                for j in graph[i]:
                    if j not in seen:seen.add(j);queue.append(j)
            fans.append(fan)
        if len(fans)!=2:return None,'contato não se divide em duas superfícies locais'
        move=min(fans,key=lambda f:(len(f),min(f)));direction=[0.0,0.0,0.0]
        for i in move:
            n=normal(vertices,triangles[i]);direction=[a+b for a,b in zip(direction,n)]
        magnitude=norm(direction)
        if magnitude<1e-12:return None,'normal local indefinida'
        newpoint=[p+SEPARATION_MM*n/magnitude for p,n in zip(vertices[v],direction)]
        if norm(sub(newpoint,vertices[v]))>SEPARATION_MM+1e-9:return None,'limite de deslocamento excedido'
        newindex=len(out);out.append(newpoint)
        for i in move:tris[i]=[newindex if x==v else x for x in tris[i]]
    # SketchUp welds equal coordinates, so index-only separation is insufficient.
    if len({tuple(round(x,8) for x in p) for p in out})!=len(out):return None,'vértices continuaram coincidentes'
    sources=list(range(len(triangles)))
    accepted,reason=_accepted(vertices,triangles,out,tris,sources,SEPARATION_MM,1e-4,check)
    if accepted is None:return None,reason
    return (out,tris,sources,dict(operation='separate_touching_fans',max_displacement_mm=SEPARATION_MM,
                                 changed_vertices=len(bad),**accepted)),None

def process_mesh(points,facets,treatment='complete',is_solid=True):
    """Return final mesh, checks, repair log and triangle provenance for colors."""
    if treatment not in ('none','conservative','complete'):raise ValueError('Tratamento inválido.')
    vertices,triangles,input_sources=_normalize(points,facets);check=audit(vertices,triangles)
    baseline={'vertices':vertices,'triangles':triangles}
    sources=list(range(len(triangles)));repairs=[];attempts=[]
    if is_solid and treatment=='complete' and check['nonmanifold'] and not check['boundary'] and not check['conflicts']:
        fixed,reason=_separate(vertices,triangles,check)
        if fixed:
            vertices,triangles,local,info=fixed;sources=[sources[i] for i in local];check=info['check'];repairs.append(info)
        else:attempts.append('Separação local rejeitada: '+reason)
    if is_solid and treatment!='none' and check['closed'] and check['thin_triangles']:
        fixed,reason=_weld(vertices,triangles,check)
        if fixed:
            vertices,triangles,local,info=fixed;sources=[sources[i] for i in local];check=info['check'];repairs.append(info)
        else:attempts.append('União de vértices rejeitada: '+reason)
    return dict(vertices=vertices,triangles=triangles,check=check,repairs=repairs,repair_attempts=attempts,
                triangle_sources=sources,input_triangle_sources=[input_sources[i] for i in sources],color_geometry=baseline)
