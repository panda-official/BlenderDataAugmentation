import bpy





class RecoverPanel(bpy.types.Panel):
    bl_idname = "RECOVER_PANEL"
    bl_label = "Recover and Save Data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw_header(self, context):
       layout = self.layout
       layout.label(text="PANDA")

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.operator("transform.save")
        box.operator("transform.restore")

class DataPanel(bpy.types.Panel):
    bl_idname = "DATA_PANEL"
    bl_label = "Data Generation"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    
    def draw_header(self, context):
       layout = self.layout
       layout.label(text="PANDA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        data_generation = scene.data_generation
        box = layout.box()
        box.label(text="Generate Data")
        row1 = box.row()
        row1.prop(data_generation, "classes_count")
        row1.prop(data_generation, "rotation_labels")
        row1.prop(data_generation, "number_of_frames")
        box.operator("render_and_bb.generate")
        row = box.row()
        row.operator("render.generate")
        row.operator("bb.generate")
        row2 = box.row()
        row2.operator("json.export")

class AugmentationPanel(bpy.types.Panel):
    bl_idname = "AUGMENTATION_PANEL"
    bl_label = "Augmentation"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    
    def draw_header(self, context):
       layout = self.layout
       layout.label(text="PANDA")

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
        row4 = box_enviro.row()
        row4.prop(data_generation, "number_of_frames_aug_enviro")
        row5 = box_enviro.row()
        row5.prop(data_generation, "lamps_strength")
        row5.prop(data_generation, "lamps_temperature")
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
        #row.operator("augment.clear")