import bpy
import bmesh
import math

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj,do_unlink = True)

Road = bmesh.new()
bmesh.ops.create_grid(Road,size = 1)

for i in range(100):
    if i % 2 == 0:
        mesh = bpy.data.meshes.new("Road")
        Road.to_mesh(mesh)
        mesh.update()

        obj = bpy.data.objects.new("Road",mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = (i,0,0)
Road.free()

Line = bmesh.new()
bmesh.ops.create_grid(Line,size = 1)

for j in range(100):
    if j % 4 == 0:
        mesh = bpy.data.meshes.new("Line")
        Line.to_mesh(mesh)
        mesh.update()

        obj = bpy.data.objects.new("Line",mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = (j,0,0.01)
        obj.scale = (0.5,0.05,1)
Line.free()

Le = bmesh.new()
bmesh.ops.create_grid(Le,size = 1)

for side in [-1,1]:
    mesh = bpy.data.meshes.new(f"Le{side}")
    Le.to_mesh(mesh)
    mesh.update()

    obj = bpy.data.objects.new(f"Le{side}",mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = (50,side * 0.75,0.01)
    obj.scale = (50,0.05,1)
Le.free()

cone = bmesh.new()
bmesh.ops.create_cone(cone,cap_ends = True,cap_tris = False,segments = 16,radius1 = 0.1,radius2 = 0.1,depth = 1.5)
cone1 = bmesh.new()
bmesh.ops.create_cone(cone1,cap_ends = True,cap_tris = False,segments = 16,radius1 = 0.75,radius2 = 0,depth = 0.5)
cone2 = bmesh.new()
bmesh.ops.create_cone(cone2,cap_ends = True,cap_tris = False,segments = 16,radius1 = 0.6,radius2 = 0,depth = 0.4)

for side in [-1,1]:
    for i in range(0,100,3):
        mesh = bpy.data.meshes.new("树干")
        cone.to_mesh(mesh)
        mesh.update()
        obj = bpy.data.objects.new("树干",mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = (i,side * 1.1,0.75)

        mesh1 = bpy.data.meshes.new("树叶1")
        cone1.to_mesh(mesh1)
        mesh1.update()
        obj1 = bpy.data.objects.new("树叶1",mesh1)
        bpy.context.collection.objects.link(obj1)
        obj1.location = (i,side * 1.1,1)

        mesh2 = bpy.data.meshes.new("树叶2")
        cone2.to_mesh(mesh2)
        mesh2.update()
        obj2 = bpy.data.objects.new("树叶2",mesh2)
        bpy.context.collection.objects.link(obj2)
        obj2.location = (i,side * 1.1,1.4)
cone.free()
cone1.free()
cone2.free()
