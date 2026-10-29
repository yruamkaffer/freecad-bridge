# Copyright (c) 2026 Yruam Kaffer de Faria
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import math
from cad_tools import inventory

def rgb(value):
    try:
        values=[float(value[i]) for i in range(3)]
        if any(not math.isfinite(v) or not 0 <= v <= 1 for v in values):return None
        return [round(v*255) for v in values]
    except (TypeError,ValueError,IndexError):return None

def signature(shape):
    b=shape.BoundBox;c=shape.CenterOfMass
    return [shape.Volume,b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax,c.x,c.y,c.z]

def matches(a,b):
    return abs(a[0]-b[0]) <= max(1e-5,abs(a[0])*1e-7) and all(abs(x-y)<1e-5 for x,y in zip(a[1:],b[1:]))

def read(source,App):
    import Import
    doc=App.newDocument('FreeCADBridgeMetadata')
    try:
        colors=Import.insert(source,doc.Name,merge=False,useLinkGroup=False,mode=0) or []
        doc.recompute()
        color_map={obj.Name:list(values) for obj,values in colors}
        records=[];visited=set()
        # Only traverse visible occurrence roots; avoid also exporting prototypes.
        def walk(obj):
            if obj.Name in visited:return
            visited.add(obj.Name)
            group=getattr(obj,'Group',None)
            if group:
                for child in group:walk(child)
                return
            if not hasattr(obj,'Shape') or obj.Shape.isNull():return
            shape=obj.Shape.copy()
            try:
                own=getattr(obj,'Placement',App.Placement())
                global_placement=obj.getGlobalPlacement()
                shape.Placement=global_placement.multiply(own.inverse()).multiply(shape.Placement)
            except Exception:pass
            values=color_map.get(obj.Name,[])
            if not values and hasattr(obj,'LinkedObject'):
                values=color_map.get(obj.LinkedObject.Name,[])
            items=inventory(shape)
            for n,(kind,solid) in enumerate(items):
                face_colors=[]
                for face in solid.Faces:
                    index=next((i for i,f in enumerate(shape.Faces) if face.isSame(f)),None)
                    col=values[0] if len(values)==1 else (values[index] if index is not None and index<len(values) else None)
                    face_colors.append(rgb(col))
                usable=[c for c in face_colors if c is not None]
                records.append({'name':obj.Label+('_%d'%(n+1) if len(items)>1 else ''),'shape':solid,'signature':signature(solid),'geometry_type':kind,'face_colors':face_colors,'color':usable[0] if usable and len(usable)==len(face_colors) and all(c==usable[0] for c in usable) else None})
        roots=[obj for obj in doc.Objects if not obj.InList]
        for obj in roots:walk(obj)
        return doc,records
    except Exception:
        App.closeDocument(doc.Name)
        raise

def choose(solid,records,kind=None):
    sig=signature(solid)
    candidates=[record for record in records if (kind is None or record.get('geometry_type','solid')==kind) and matches(sig,record['signature'])]
    if len(candidates)==1:return candidates[0]
    # Identical overlapping occurrences are ambiguous; never silently mislabel.
    return None

def triangle_key(points):
    return tuple(sorted(tuple(round(float(v),6) for v in p) for p in points))

def transfer_colors(result,original,record,tolerance):
    if record['color'] is not None:
        result['color']=record['color'];return 0
    if not any(c is not None for c in record['face_colors']):return len(result['triangles'])
    # Cache lookup by triangle geometry. Unmatched triangles remain unpainted.
    lookup={}
    for face,color in zip(record['shape'].Faces,record['face_colors']):
        if color is None:continue
        points,facets=face.tessellate(tolerance)
        for t in facets:
            key=triangle_key([[points[i].x,points[i].y,points[i].z] for i in t])
            lookup[key]=color
    result['triangle_colors']=[lookup.get(triangle_key([result['vertices'][i] for i in t])) for t in result['triangles']]
    return sum(c is None for c in result['triangle_colors'])
