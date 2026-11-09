import bpy
import bmesh
import math

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj,do_unlink = True) #删除所有物体

cb = bmesh.new()   #定义变量cb
bmesh.ops.create_cube(cb,size = 1)

for i in range(0,100,2):
    cube_mesh = bpy.data.meshes.new("立方体")
    cb.to_mesh(cube_mesh)
    cube_mesh.update()

    obj = bpy.data.objects.new("立方体",cube_mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = (i,0,0)  #位置x,y,z
    obj.rotation_euler = (0,0,math.radians(45)) #旋转
    obj.scale = (1,1,1) #缩放

cb.free()
