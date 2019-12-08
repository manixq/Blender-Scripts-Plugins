
#By Manixus Decimus Keksimus

import bpy
from mathutils import Matrix, Vector
import bmesh
from bpy.types import Menu
import rna_keymap_ui


bl_info = {
    "blender": (2, 81, 0),
    "name": "Color Changer",
    "category": "Edit",
}

import bpy



class MaterialColorChanger(bpy.types.Operator):
    """MaterialColorChanger"""
    bl_idname = "object.materialcolorchanger"
    bl_label = "MaterialColorChanger"
    bl_options = {'REGISTER', 'UNDO'}

    lBaseColor : bpy.props.FloatVectorProperty(name="Base_Color", subtype='COLOR', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, description="color picker")

    def execute(self, context):
        context = bpy.context

        lSelectedObjects = bpy.context.selected_objects
        for lObject in lSelectedObjects:
            for lMaterialSlotlot in lObject.material_slots:
                # bpy.data.materials[lMaterialSlotlot.name].use_nodes = True
                bpy.data.materials[lMaterialSlotlot.name].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (self.lBaseColor.r, self.lBaseColor.g, self.lBaseColor.b, 1.0)

        return{'FINISHED'}


# store keymaps here to access after registration
addon_keymaps = []

def menu_draw(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(MaterialColorChanger.bl_idname)

def register():
    bpy.utils.register_class(MaterialColorChanger)
    bpy.types.VIEW3D_MT_object.prepend(menu_draw)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(MaterialColorChanger.bl_idname, 'NUMPAD_0', 'PRESS', ctrl=False, shift=True)
    addon_keymaps.append(km)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_draw)
    bpy.utils.unregister_class(MaterialColorChanger)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()