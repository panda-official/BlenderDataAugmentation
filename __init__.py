
bl_info = {
    "name": "Data Augmentation",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "PANDA",
}

import bpy

from . import settings 
from . import operators
from . import ui


def menu_func(self, context):
    self.layout.operator(operators.BbGenerate.bl_idname)
    self.layout.operator(operators.RenderGenerate.bl_idname)

classes = (
    operators.SaveTransformOperator,
    operators.RestoreTransform,
    operators.BbGenerate,
    operators.RenderGenerate,
    operators.RenderAndBbGenerate,
    operators.AugmentGenerate,
    operators.JsonExport,
    operators.AugmentGenerateEnviro,
    settings.GenerationSettings,
    ui.RecoverPanel,
    ui.DataPanel,
    ui.AugmentationPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.
    bpy.types.Scene.data_generation = bpy.props.PointerProperty(type=settings.GenerationSettings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



