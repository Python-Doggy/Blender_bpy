import bpy
import bmesh
import math
import random

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

def random_val():
    s = random.random()
    if s > 0.5:
        return random.uniform(-4,-2)
    else:
        return random.uniform(2,4)
stone = bmesh.new()
bmesh.ops.create_uvsphere(stone,u_segments = 32,v_segments = 16,radius = 0.4)

for x in range(100):
    stone_mesh = bpy.data.meshes.new("Stone")
    stone.to_mesh(stone_mesh)
    stone_mesh.update()

    obj = bpy.data.objects.new("Stone",stone_mesh)
    bpy.context.collection.objects.link(obj)
    z = random.uniform(0.5,1.5)
    obj.scale = (random.uniform(0.5,2),random.uniform(0.5,2),1)
    obj.location = (random.uniform(0,100),random_val(),z * 0.2)
stone.free()

grass1 = bmesh.new()
bmesh.ops.create_grid(grass1,size = 0.4)
grass2 = bmesh.new()
bmesh.ops.create_grid(grass2,size = 0.4)


for j in range(100):
    grass_mesh1 = bpy.data.meshes.new(f"Grass1{j}")
    grass_mesh2 = bpy.data.meshes.new(f"Grass2{j}")
    grass1.to_mesh(grass_mesh1)
    grass2.to_mesh(grass_mesh2)
    grass_mesh1.update()
    grass_mesh2.update()

    obj1 = bpy.data.objects.new(f"Grass1{j}",grass_mesh1)
    obj2 = bpy.data.objects.new(f"Grass2{j}",grass_mesh2)
    bpy.context.collection.objects.link(obj1)
    bpy.context.collection.objects.link(obj2)

    z_rot = random.uniform(0,90)
    x_loc = random.uniform(0,100)
    obj1.rotation_euler = (math.radians(90),0,z_rot)
    obj2.rotation_euler = (0,math.radians(90),z_rot)
    obj1.location = (x_loc,random_val(),0.2)
    obj2.location = (x_loc,random_val(),0.2)
grass1.free()
grass2.free()
