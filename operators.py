import bpy
import bpy_extras
import math
import mathutils
import random
import numpy as np
import json 
import copy
from . import settings
from . import utils

class SaveTransformOperator(bpy.types.Operator):
    """Save Transform"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "transform.save"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Save Transform"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        global saved 
        utils.save(saved)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

class RestoreTransform(bpy.types.Operator):
    """Restore Transform"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "transform.restore"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Restore Transform"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        global saved
        utils.restore(saved)
        return {'FINISHED'}        # Lets Blender know the operator finished successfully

class JsonExport(bpy.types.Operator):
    """Export JSON"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "json.export"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Export JSON"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        scene = context.scene
        fp = scene.render.filepath
        with open(fp + 'data' + '.json', 'w') as outfile:
            json.dump(settings.GenerationSettings.dict_main, outfile, indent=4)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

class BbGenerate(bpy.types.Operator):
    """Generate bounding boxes"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "bb.generate"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate BBs"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        task = "bb"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.number_of_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(task, rotation_labels, scene, number_of_frames, classes_count)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

class RenderGenerate(bpy.types.Operator): 
    """Generate Renders"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "render.generate"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Renders"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        task = "render"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.number_of_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(task, rotation_labels, scene, number_of_frames, classes_count)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

class AugmentGenerate(bpy.types.Operator): 
    """Augment selected class"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "augment.generate"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Augment class"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        task = "generate"
        scene = context.scene
        number_of_frames = scene.data_generation.number_of_frames_aug
        class_to_aug = scene.collection_to_augment
        utils.augment(task, scene, number_of_frames, class_to_aug)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

class AugmentGenerateEnviro(bpy.types.Operator):
    """Augment Envirorment"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "augment.generate_enviro"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Augment Envirorment"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        scene = context.scene
        number_of_frames = scene.data_generation.number_of_frames_aug_enviro
        utils.augment_enviro(scene, number_of_frames, "augment")

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

class RenderAndBbGenerate(bpy.types.Operator):
    """Generate Renders"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "render_and_bb.generate"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Renders and BBs"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        task = "bb+render"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.number_of_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(task, rotation_labels, scene, number_of_frames, classes_count)

        return {'FINISHED'}            # Lets Blender know the operator finished successfully

saved = utils.StoreTransform()