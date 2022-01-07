import bpy
import bpy_extras
import math
import mathutils
import random
import numpy as np
import json 
import copy
from . import settings 


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )

def get_rotation_matrix(obj):

    #get object rotation in euler
    rot_euler = obj.rotation_euler 
    #convert euler rotation to rotation matrix
    rotation_matrix = mathutils.Euler(rot_euler).to_matrix()

    #create string with rotation matrix    
    matrix_string = ""
    for k in range(3):
        matrix_string += str(rotation_matrix[0][k]) + " " + str(rotation_matrix[1][k]) + " " + str(rotation_matrix[2][k]) + " "
    matrix_string = matrix_string[:-1]

    return matrix_string
    
def generate_bb_and_render(task, rotation_labels, scene, number_of_frames, classes_count):
    
    fp = scene.render.filepath # get existing output path
    print(fp)
    scene.render.image_settings.file_format = 'PNG' # set output format to .png
        
    for i in range(1, number_of_frames):
        if (i==0):
            continue
        # set current frame
        scene.frame_set(i)
        # set output path so render won't get overwritten
        scene.render.filepath = fp + str(i)       
        
        # Render Frame if mode set to "render" or "bb+render"
        if (task != "bb"):
            bpy.ops.render.render(write_still=True)
        
        # Bounding Box information:
        camera = bpy.data.collections['Camera'].all_objects[0]
        
        
        
        with open(fp + str(i) + '.txt','w+') as datei:
            for k in range(0, classes_count): 

                objs = bpy.data.collections[f"Class{k}"].all_objects

                for obj in objs:

                    location = camera_view_bounds_2d(scene, camera, obj)
                        
                    x,y,w,h = location
                    if (x==0 and y==0 and w==0 and h==0):
                        continue
                    x = x + (w/2)
                    y = y + (h/2)
                    x_norm = round(x/scene.render.resolution_x, 6)
                    y_norm = round(y/scene.render.resolution_y, 6)
                    w_norm = round(w/scene.render.resolution_x, 6)
                    h_norm = round(h/scene.render.resolution_y, 6)     
                    
                    if (rotation_labels==True):
                        matrix_string = get_rotation_matrix(obj)
                    else:
                        matrix_string = ""
                    
                    line = str(k)+' '+str(x_norm)+' '+str(y_norm)+' '+str(w_norm)+' '+str(h_norm)+' '+matrix_string+ '\n'
                    datei.write(line)
        
        
    # restore the filepath
    scene.render.filepath = fp

    # Set Scene
    scene = bpy.context.scene   

def rand_transform(x, y, z, task):
    
    if (task == "loc"):
        transform = np.array([random.uniform(x/-2, x/2), random.uniform(y/-2, y/2), random.uniform(z/-2, z/2)])
    elif (task == "scale"):
        transform = np.array([random.uniform(x/-2 + 1, x/2 + 1), random.uniform(y/-2 + 1, y/2 + 1), random.uniform(z/-2 + 1, z/2 + 1)])
    elif (task == "rot"):
        x = x * math.pi / 180 
        y = y * math.pi / 180
        z = z * math.pi / 180 
        transform = np.array([random.uniform(x/-2, x/2), random.uniform(y/-2, y/2), random.uniform(z/-2, z/2)])
    return transform

def augment(task, scene, number_of_frames, class_to_aug):

    if (task == "generate"): 

        objs = class_to_aug.all_objects

        for obj in objs:
            object_initial_location = obj.location
            for i in range(1, number_of_frames):
                obj.rotation_euler = rand_transform(scene.data_generation.rotation_variation_X, scene.data_generation.rotation_variation_Y, scene.data_generation.rotation_variation_Z, "rot")
                obj.keyframe_insert(data_path="rotation_euler", frame= i)
                obj.location = object_initial_location[:] + rand_transform(scene.data_generation.translation_variation_X, scene.data_generation.translation_variation_Y, scene.data_generation.translation_variation_Z, "loc")
                obj.keyframe_insert(data_path="location", frame= i)
                obj.scale = rand_transform(scene.data_generation.scale_variation_X, scene.data_generation.scale_variation_Y, scene.data_generation.scale_variation_Z, "scale")
                obj.keyframe_insert(data_path="scale", frame= i)

        class_to_aug_str = (str(class_to_aug)) 
        class_to_aug_str = class_to_aug_str.split('"')[1]
        augment_dict = {
            f'translation variations {class_to_aug_str}': str(scene.data_generation.translation_variation_X) + ' ' + str(scene.data_generation.translation_variation_Y) + ' ' + str (scene.data_generation.translation_variation_Z),
            f'rotation variations {class_to_aug_str}': str(scene.data_generation.rotation_variation_X) + ' ' + str(scene.data_generation.rotation_variation_Y) + ' ' + str (scene.data_generation.rotation_variation_Z),
            f'scale variations {class_to_aug_str}': str(scene.data_generation.scale_variation_X) + ' ' + str(scene.data_generation.scale_variation_Y) + ' ' + str (scene.data_generation.scale_variation_Z),
            f'augmented frames {class_to_aug_str}': number_of_frames
        }
        dict_add(augment_dict)

def augment_enviro(scene, number_of_frames, task):

    empty = bpy.data.collections['Lights'].objects['Empty']
    plane = bpy.data.collections['Lights'].objects['PlaneLamp']
    spot = bpy.data.collections['Lights'].objects['Spot']

    empty_init_loc = empty.location
    plane_init_loc = plane.location
    spot_init_loc = spot.location
    init_plane_strenght = 5.0
    init_spot_strenght = 8.0
    init_plane_temperature = 7500.0
    init_spot_temperature = 6500.0

    plane_strenght = bpy.data.materials["PLANE_MAT"].node_tree.nodes["Emission"].inputs[1]
    spot_strenght = bpy.data.lights["Spot"].node_tree.nodes["Emission"].inputs[1]
    plane_temperature = bpy.data.materials["PLANE_MAT"].node_tree.nodes["Blackbody"].inputs[0]
    spot_temperature = bpy.data.lights["Spot"].node_tree.nodes["Blackbody"].inputs[0]

    if (task == "augment"):
        for i in range(1, number_of_frames):

            #empty augmentation
            empty.location = empty_init_loc[:] + rand_transform(0, 0, scene.data_generation.empty_z_variation/5, "loc")
            empty.keyframe_insert(data_path="location", frame = i)
            empty.rotation_euler = rand_transform(0, 0, scene.data_generation.empty_z_variation_rot, "rot")
            empty.keyframe_insert(data_path="rotation_euler", frame= i)

            #lamps jitter
            plane.location = plane_init_loc[:] + rand_transform(scene.data_generation.lamps_jitter / 10, scene.data_generation.lamps_jitter / 10, scene.data_generation.lamps_jitter / 10, "loc")
            plane.keyframe_insert(data_path="location", frame = i)
            spot.location = spot_init_loc[:] + rand_transform(scene.data_generation.lamps_jitter / 10, scene.data_generation.lamps_jitter / 10, scene.data_generation.lamps_jitter / 10, "loc")
            spot.keyframe_insert(data_path="location", frame = i)

            #lamps strength
            
            plane_strenght.default_value = init_plane_strenght - init_plane_strenght * random.uniform(scene.data_generation.lamps_strength/-2 , scene.data_generation.lamps_strength/2)
            plane_strenght.keyframe_insert(data_path="default_value", frame = i)
            spot_strenght.default_value = init_spot_strenght - init_spot_strenght * random.uniform(scene.data_generation.lamps_strength/-2 , scene.data_generation.lamps_strength/2)
            spot_strenght.keyframe_insert(data_path="default_value", frame = i)

            #lamps temperture
            
            plane_temperature.default_value = init_plane_temperature - init_plane_temperature * random.uniform(scene.data_generation.lamps_temperature/-2 , scene.data_generation.lamps_temperature/2)
            plane_temperature.keyframe_insert(data_path="default_value", frame = i)
            spot_temperature.default_value = init_spot_temperature - init_spot_temperature * random.uniform(scene.data_generation.lamps_temperature/-2 , scene.data_generation.lamps_temperature/2)
            spot_temperature.keyframe_insert(data_path="default_value", frame = i)

        augment_enviro_dict = {
                'z variation empty': scene.data_generation.empty_z_variation,
                'rotation variation empty': scene.data_generation.empty_z_variation_rot,
                'jitter': scene.data_generation.lamps_jitter,
                'augmented frames envirorment': number_of_frames,
                'strength variation': scene.data_generation.lamps_strength,
                'temperature variation': scene.data_generation.lamps_temperature
            }
        dict_add(augment_enviro_dict)

    elif (task == "clear"):

        bpy.data.materials["PLANE_MAT"].node_tree.animation_data_clear()
        bpy.data.lights["Spot"].node_tree.animation_data_clear()

        #set default values   
        plane_strenght.default_value = init_plane_strenght
        spot_strenght.default_value = init_plane_strenght
        spot_temperature.default_value = init_spot_temperature 
        plane_temperature.default_value = init_plane_temperature

def dict_add(dict):
    settings.GenerationSettings.dict_main |= dict  

class StoreTransform:

    def __init__(self):
        #bpy.data.scenes['Scene'].frame_set(1)
        self.update()

    def update(self):
        objs = bpy.data.collections['DATA'].all_objects
        self.locations = [copy.copy(obj.location) for obj in objs]
        self.rotations = [copy.copy(obj.rotation_euler) for obj in objs]
        self.scale = [copy.copy(obj.scale) for obj in objs]

def create():
    created = StoreTransform()
    return created

def save(saved):
    bpy.data.scenes['Scene'].frame_set(1)
    saved.update()
    
def restore(saved):
    objs = bpy.data.collections['DATA'].all_objects
    scene = bpy.data.scenes['Scene']  
    augment_enviro(scene, 0, "clear")
    for i, obj in enumerate(objs):
        obj.animation_data_clear()
        obj.location = saved.locations[i]
        obj.rotation_euler = saved.rotations[i]
        obj.scale = saved.scale[i]
