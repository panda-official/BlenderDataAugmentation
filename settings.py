import bpy
import bpy_extras
import math
import mathutils
import random
import numpy as np
import json 
import copy

from . import utils


class GenerationSettings(bpy.types.PropertyGroup):

    #Generation Settings

    rotation_labels : bpy.props.BoolProperty(
        name="Rotation labels",
        description="Enable roation matrix labels generation",
        default = False
        )

    number_of_frames : bpy.props.IntProperty(
        name = "Frames",
        description="number of frames to render/generate BBs",
        default = 5,
        min = 1,
        max = 100000
        )
    
    classes_count : bpy.props.IntProperty(
        name = "Classes",
        description="number of classes",
        default = 1,
        min = 1,
        max = 100
        )
    
    #Data Augmentation Settings

    number_of_frames_aug : bpy.props.IntProperty(
        name = "Frames",
        description="Frames to Augment Objects",
        default = 5,
        min = 1,
        max = 250000
        )

    rotation_variation_X : bpy.props.FloatProperty(
        name = "X",
        description="Variation of rotation in X axis in degrees",
        default = 0,
        min = 0,
        max = 360
        )

    rotation_variation_Y : bpy.props.FloatProperty(
        name = "Y",
        description="Variation of rotation in Y axis in degrees",
        default = 0,
        min = 0,
        max = 360
        )

    rotation_variation_Z : bpy.props.FloatProperty(
        name = "Z",
        description="Variation of rotation in Z axis in degrees",
        default = 0,
        min = 0,
        max = 360
        )
    translation_variation_X : bpy.props.FloatProperty(
        name = "X",
        description="Variation of translation in X axis in meters",
        default = 0,
        min = 0,
        max = 2
        )

    translation_variation_Y : bpy.props.FloatProperty(
        name = "Y",
        description="Variation of translation in Y axis in meters",
        default = 0,
        min = 0,
        max = 2
        )

    translation_variation_Z : bpy.props.FloatProperty(
        name = "Z",
        description="Variation of translation in Z axis in meters",
        default = 0,
        min = 0,
        max = 2
        )
    
    scale_variation_X : bpy.props.FloatProperty(
        name = "X",
        description="Variation of scale in X axis in degrees",
        default = 0,
        min = 0,
        max = 2
        )

    scale_variation_Y : bpy.props.FloatProperty(
        name = "Y",
        description="Variation of scale in Y axis in degrees",
        default = 0,
        min = 0,
        max = 2
        )

    scale_variation_Z : bpy.props.FloatProperty(
        name = "Z",
        description="Variation of scale in Z axis in degrees",
        default = 0,
        min = 0,
        max = 2
        )

    
    bpy.types.Scene.collection_to_augment = bpy.props.PointerProperty(
        name="Class to Augment",
        type=bpy.types.Collection)

    #Envirorment Augmentation Settings

    number_of_frames_aug_enviro: bpy.props.IntProperty(
        name = "Frames",
        description="Frames to augment envirorment",
        default = 5,
        min = 1,
        max = 100000
    )

    empty_z_variation: bpy.props.FloatProperty(
        name = "position",
        description="Variation of Z position of all lamps",
        default = 0,
        min = 0,
        max = 1
        )

    empty_z_variation_rot: bpy.props.FloatProperty(
        name = "Z rotation variation",
        description="Variation of Z rotation of all lamps",
        default = 0,
        min = 0,
        max = 360
        )

    lamps_jitter : bpy.props.FloatProperty(
        name = "jitter",
        description="Jitter for all lamps",
        default = 0,
        min = 0,
        max = 1
        )

    lamps_temperature : bpy.props.FloatProperty(
        name = "temperature",
        description="temperatur variation for all lamps",
        default = 0,
        min = 0,
        max = 1
        )

    lamps_strength : bpy.props.FloatProperty(
        name = "strength",
        description="strenght variation for all lamps",
        default = 0,
        min = 0,
        max = 1
        )
        
    dict_main = {}