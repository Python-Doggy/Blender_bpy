import bpy
import bmesh

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj,do_unlink = True)

def create_floor(name : str = "UCX_Floor",location : tuple = (0,0,0),scale : tuple = (0,0,0)):
    floor = bmesh.new()
    bmesh.ops.create_cube(floor,size = 1)

    floor_mesh = bpy.data.meshes.new(name)
    floor.to_mesh(floor_mesh)
    floor_mesh.update()
    floor.free()

    obj_floor = bpy.data.objects.new(name,floor_mesh)
    bpy.context.collection.objects.link(obj_floor)
    obj_floor.location = location
    obj_floor.scale = scale
    return obj_floor

def create_wall(name : str = "UCX_Wall",location : tuple = (0,0,0),scale : tuple = (0,0,0)):
    wall = bmesh.new()
    bmesh.ops.create_cube(wall,size = 1)

    wall_mesh = bpy.data.meshes.new("UCX_Wall")
    wall.to_mesh(wall_mesh)
    wall_mesh.update()
    wall.free()

    obj_wall = bpy.data.objects.new("UCX_Wall",wall_mesh)
    bpy.context.collection.objects.link(obj_wall)
    obj_wall.location = location
    obj_wall.scale = scale
    return obj_wall

for center in range(3):#中心大厅
    create_floor(name="UCX_floor_Center",location = (0,0.5,3.5 * center),scale = (30,15,0.2))
    create_floor(name="UCX_Floor_Meeting",location= (-4,11,center * 3.5),scale= (16,6,0.2))
    create_floor(name= "UCX_Floor_Stair",location= (6,11,center * 3.5),scale= (4,6,0.2))
for left_floor in range(6):
    for side in [-1,1]:
        create_floor(name="UCX_Floor",location=(-27 * side,8,left_floor * 3.5),scale = (24,43,0.2))
        create_floor(name = "UCX_Floor",location=(-20 * side,-24.5,left_floor * 3.5),scale= (10,22,0.2))
        if left_floor < 5:
            create_floor(name= "UCX_Floor",location= (-13 ,-34.25,left_floor * 3.5),scale= (4,2.5,0.2))
        if left_floor < 4:
            create_floor(name="UCX_Floor", location=(-13 , -28.75, (left_floor + 1) * 3.5 - 1.75), scale=(4, 2.5, 0.2))
        if left_floor == 5:
            create_floor(name= "UCX_Floor",location= (-13  , -31.5,17.5),scale= (4,8,0.2))

for center_wall in range(2):
    for side_wall in [-1,1]:
        create_wall(name= "UCX_Wall_Center",location= (-9.5 * side_wall,-7,center_wall * 3.5 + 1.75),scale= (11,0.2,3.5))
        create_wall(name = "UCX_Wall_Center2",location= (0,-7 ,center_wall * 3.5 + 2.75),scale = (8,0.2,1.5))

for left_room in range(5):
    create_wall(name = "UCX_Wall_WC",location= (-17.5,-30,left_room * 3.5 + 1.65),scale= (0.2,9,3.5))
    create_wall(name = "UCX_Wall_Office",location= (-17.5,-25,left_room * 3.5 + 1.65),scale= (0.2,1,3.5))
    create_wall(name = "UCX_Wall_Office",location= (-17.5,-19,left_room * 3.5 + 1.65),scale = (0.2,8,3.5))
    create_wall(name = "UCX_Wall_Office",location= (-17.5,-13.75,left_room * 3.5 + 1.65),scale = (0.2,0.5,3.5))
    create_wall(name = "UCX_Wall_Office",location= (-21.2,-13.5,left_room * 3.5 + 1.65),scale = (7.4,0.2,3.5))
    create_wall(name="UCX_Wall_Office", location=(-21.2, -25.4, left_room * 3.5 + 1.65), scale=(7.4, 0.2, 3.5))
    create_wall(name = "UCX_Wall_Class",location= (-17.5,-9.5,left_room * 3.5 + 1.65),scale= (0.2,8,3.5))
    create_wall(name = "UCX_Wall_Class",location= (-18.1,-5.6,left_room * 3.5 + 1.65),scale= (1,0.2,3.5))
    create_wall(name="UCX_Wall_Class", location=(-22.6, -5.6, left_room * 3.5 + 1.65), scale=(6,0.2, 3.5))
    create_wall(name="UCX_Wall_Class", location=(-27.35, -5.6, left_room * 3.5 + 1.65), scale=(1.5, 0.2, 3.5))
    create_wall(name="UCX_Wall_Class", location=(-27.35, -5.6, left_room * 3.5 + 1.65), scale=(1.5, 0.2, 3.5))
