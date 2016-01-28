# Mesh_ReEnter
various ways to create a mesh and pick it up later for parametric modification

The point of this repo is to show approaches to this problem. Ideally the scripts shouldn't register bpy.types.Object.*  collections or properties --- tho this limitation is a little bit arbitrary .

```python

    # upon creation
    obj['kind'] = 'circle'

    # upon registration
    bpy.types.Object.parametric_circle =   # PropertyGroup

    # upon draw() in a panel
    row = layout.row()
    kind = obj.get('kind')
    if kind in ['circle', 'gear', 'bolt', 'diamond']:
        props = getattr(obj, 'parametric_' + kind)
        if props:
            col = l.column()
            
            for propname in props.rna_type.properties.keys():
                if not propname in {'rna_type', 'name'}:
                    col.prop(props, propname)
       
```
