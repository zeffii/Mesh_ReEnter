bl_info = {
    "name": "parametric circle",
    "author": "Dealga McArdle",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "category": "3D View"
}

import bpy 
import bmesh

import math
from math import sin, cos, pi

def make_geom(props):
    r = props.radius
    num = props.verts
    theta = 2 * pi / num
    vertices = [(sin(i*theta)*r, cos(i*theta)*r, 0) for i in range(num)]
    edges = [(i, i+1) for i in range(num-1)] + [(num-1, 0)]
    return vertices, edges

def add_obj_to_scene(obj, active=True):
    scene = bpy.context.scene
    scene.objects.link(obj)
    if active:
        scene.objects.active = obj

def update_mesh(obj, wipe=False):
    mesh = obj.data

    if wipe:
        bm = bmesh.new()
        bm.to_mesh(mesh)
        mesh.update()

    verts, edges = make_geom(obj.circle_props)
    mesh.from_pydata(verts, edges, [])
    mesh.update()


def update_object(self, context):
    obj = context.active_object 
    update_mesh(obj, wipe=True)


class CircleProps(bpy.types.PropertyGroup):
    radius = bpy.props.FloatProperty(default=1.0, min=0.01, max=6.0, update=update_object)
    verts = bpy.props.IntProperty(default=8, min=3, update=update_object)


class CircleGen(bpy.types.Operator):
    bl_idname = "circlegen.make_circle"
    bl_label = "Make A new Circle"

    def make_me(self, context):
        ID = str(hash(self))
        mesh = bpy.data.meshes.new("mesh_name_" + ID)
        obj = bpy.data.objects.new("obj_name", mesh)
        obj['ID'] = ID
        update_mesh(obj)
        add_obj_to_scene(obj)

    def execute(self, context):
        self.make_me(context)

        return {'FINISHED'}

class CirclePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        l = self.layout

        obj = context.active_object
        if not obj:
            r = l.row()
            r.operator('circlegen.make_circle')

        else:
            ID = obj.get('ID')
            if ID:
                l.label(ID)
                r = l.row()
                r.prop(obj.circle_props, 'radius')
                r.prop(obj.circle_props, 'verts')
            else:
                l.label('not a dynamic object')
                r = l.row()
                r.operator('circlegen.make_circle')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Object.circle_props = bpy.props.PointerProperty(
        name="circle_props", type=CircleProps
    )


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.circle_props
