# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

from collections import defaultdict, deque

def prepare(points, facets):
    vertices=[]; mapping=[]; lookup={}
    for p in points:
        xyz=[float(p[0]),float(p[1]),float(p[2])]
        key=tuple(round(n,8) for n in xyz)
        if key not in lookup:
            lookup[key]=len(vertices);vertices.append(xyz)
        mapping.append(lookup[key])
    triangles=[];seen=set()
    for facet in facets:
        t=[mapping[i] for i in facet];key=tuple(sorted(t))
        if len(set(t))<3 or key in seen:continue
        seen.add(key);triangles.append(t)
    adjacency=defaultdict(list)
    for i,t in enumerate(triangles):
        for a,b in zip(t,t[1:]+t[:1]):
            adjacency[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
    graph=defaultdict(list)
    for links in adjacency.values():
        if len(links)==2:
            (a,da),(b,db)=links
            graph[a].append((b,-da*db));graph[b].append((a,-da*db))
    orientation={};components=[];conflicts=0
    for start in range(len(triangles)):
        if start in orientation:continue
        orientation[start]=1; queue=deque([start]);component=[]
        while queue:
            i=queue.popleft();component.append(i)
            for j,rel in graph[i]:
                wanted=orientation[i]*rel
                if j in orientation:
                    conflicts+=orientation[j]!=wanted
                else:orientation[j]=wanted;queue.append(j)
        components.append(component)
    for i,direction in orientation.items():
        if direction<0:triangles[i].reverse()
    volume6=0
    for t in triangles:
        p,q,r=[vertices[j] for j in t]
        volume6+=sum(p[k]*(q[(k+1)%3]*r[(k+2)%3]-q[(k+2)%3]*r[(k+1)%3]) for k in range(3))
    if volume6<0:
        for t in triangles:t.reverse()
    boundary=sum(len(v)==1 for v in adjacency.values())
    nonmanifold=sum(len(v)>2 for v in adjacency.values())
    valid=bool(triangles) and boundary==0 and nonmanifold==0 and conflicts==0
    return vertices,triangles,{'closed':valid,'boundary':boundary,'nonmanifold':nonmanifold,'conflicts':conflicts}
