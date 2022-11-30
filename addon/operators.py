import bpy

import numpy as np
import json

from . import settings
from . import utils


class LoadData(bpy.types.Operator):
    """Load JSON and augment data and envirorment"""

    bl_idname = "load.data"
    bl_label = "Augment from JSON"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        utils.load_json(scene)
        return {"FINISHED"}


class SaveTransformOperator(bpy.types.Operator):
    """Save Transform"""

    bl_idname = "transform.save"
    bl_label = "Save Transform"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        global saved
        if saved == None:
            saved = utils.create()
        else:
            utils.save(saved)
        return {"FINISHED"}


class RestoreTransform(bpy.types.Operator):
    """Restore Transform"""

    bl_idname = "transform.restore"
    bl_label = "Restore Transform"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        global saved
        utils.restore(saved)
        return {"FINISHED"}


class JsonExport(bpy.types.Operator):
    """Export JSON"""

    bl_idname = "json.export"
    bl_label = "Export JSON"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        scene = context.scene
        fp = scene.render.filepath
        with open(fp + "data" + ".json", "w") as outfile:
            json.dump(settings.GenerationSettings.dict_main, outfile, indent=4)

        return {"FINISHED"}


class BbGenerate(bpy.types.Operator):
    """Generate bounding boxes"""

    bl_idname = "bb.generate"
    bl_label = "Generate BBs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        task = "bb"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.number_of_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(
            task, rotation_labels, scene, number_of_frames, classes_count
        )

        return {"FINISHED"}


class RenderGenerate(bpy.types.Operator):
    """Generate Renders"""

    bl_idname = "render.generate"
    bl_label = "Generate Renders"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        task = "render"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.number_of_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(
            task, rotation_labels, scene, number_of_frames, classes_count
        )

        return {"FINISHED"}


class AugmentGenerate(bpy.types.Operator):
    """Augment selected class"""

    bl_idname = "augment.generate"
    bl_label = "Augment class"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        task = "generate"
        scene = context.scene
        number_of_frames = scene.data_generation.number_of_frames_aug
        class_to_aug = scene.collection_to_augment
        utils.augment(task, scene, number_of_frames, class_to_aug)

        return {"FINISHED"}


class AugmentGenerateEnviro(bpy.types.Operator):
    """Augment Envirorment"""

    bl_idname = "augment.generate_enviro"
    bl_label = "Augment Envirorment"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        scene = context.scene
        number_of_frames = scene.data_generation.number_of_frames_aug_enviro
        utils.augment_enviro(scene, number_of_frames, "augment")

        return {"FINISHED"}


class RenderAndBbGenerate(bpy.types.Operator):
    """Generate Renders"""

    bl_idname = "render_and_bb.generate"
    bl_label = "Generate Renders and BBs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        task = "bb+render"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.number_of_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(
            task, rotation_labels, scene, number_of_frames, classes_count
        )

        return {"FINISHED"}


class PreviewGenerate(bpy.types.Operator):
    """Generate Previews with Bounding Boxes"""

    bl_idname = "preview.generate"
    bl_label = "Preview"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        task = "preview"
        scene = context.scene
        rotation_labels = context.scene.data_generation.rotation_labels
        number_of_frames = context.scene.data_generation.preview_frames
        classes_count = context.scene.data_generation.classes_count
        utils.generate_bb_and_render(
            task, rotation_labels, scene, number_of_frames, classes_count
        )
        return {"FINISHED"}


saved = None
