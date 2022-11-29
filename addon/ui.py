import bpy


class RecoverPanel(bpy.types.Panel):
    bl_idname = "RECOVER_PANEL"
    bl_label = "Recover and Save Data"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="DATA AUGMENTATION")

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.operator("transform.save")
        box.operator("transform.restore")


class LoadPanel(bpy.types.Panel):
    bl_idname = "LOAD_PANEL"
    bl_label = "Load from file"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="DATA AUGMENTATION")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data_generation = scene.data_generation
        box = layout.box()
        row = box.row()
        row.prop(data_generation, "json_path")
        row.operator("load.data")


class DataPanel(bpy.types.Panel):
    bl_idname = "DATA_PANEL"
    bl_label = "Data Generation"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="DATA AUGMENTATION")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data_generation = scene.data_generation
        box = layout.box()
        box.label(text="Generation Settings")
        row1 = box.row()
        row1.prop(data_generation, "classes_count")
        row1.prop(data_generation, "rotation_labels")
        row1.prop(data_generation, "number_of_frames")
        box1 = layout.box()
        box1.label(text="Preview")
        row3 = box1.row()
        row3.prop(data_generation, "preview_frames")
        row3.prop(data_generation, "res_scale")
        row4 = box1.row()
        row4.operator("preview.generate")
        box2 = layout.box()
        box2.label(text="Generate")
        box2.operator("render_and_bb.generate")
        row = box2.row()
        row.operator("render.generate")
        row.operator("bb.generate")
        row2 = box2.row()
        row2.operator("json.export")


class AugmentationPanel(bpy.types.Panel):
    bl_idname = "AUGMENTATION_PANEL"
    bl_label = "Augmentation"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="DATA AUGMENTATION")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data_generation = scene.data_generation

        box_enviro = layout.box()
        box_enviro.label(text="Augment Envirorment")
        row3 = box_enviro.row()
        row3.prop(data_generation, "empty_z_variation_rot")
        row3.prop(data_generation, "empty_z_variation")
        row3.prop(data_generation, "lamps_jitter")
        row5 = box_enviro.row()
        row5.prop(data_generation, "lamps_strength")
        row5.prop(data_generation, "lamps_temperature")
        row4 = box_enviro.row()
        row4.prop(data_generation, "number_of_frames_aug_enviro")
        row6 = box_enviro.row()
        row6.operator("augment.generate_enviro")

        box = layout.box()
        box.label(text="Augment Data")
        box.label(text="Rotation Variation")
        row1 = box.row()
        row1.prop(data_generation, "rotation_variation_X")
        row1.prop(data_generation, "rotation_variation_Y")
        row1.prop(data_generation, "rotation_variation_Z")
        box.label(text="Translation Variation")
        row2 = box.row()
        row2.prop(data_generation, "translation_variation_X")
        row2.prop(data_generation, "translation_variation_Y")
        row2.prop(data_generation, "translation_variation_Z")
        box.label(text="Scale Variation")
        row3 = box.row()
        row3.prop(data_generation, "scale_variation_X")
        row3.prop(data_generation, "scale_variation_Y")
        row3.prop(data_generation, "scale_variation_Z")
        box.prop(data_generation, "number_of_frames_aug")
        box.prop(scene, "collection_to_augment")
        row = box.row()
        row.operator("augment.generate")
        # row.operator("augment.clear")
