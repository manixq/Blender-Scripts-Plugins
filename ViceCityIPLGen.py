
#By Manixus Decimus Keksimus

import bpy
from mathutils import Matrix, Vector
import bmesh
from bpy.types import Menu
import rna_keymap_ui


bl_info = {
    "blender": (2, 81, 0),
    "name": "Vice City IPL generator",
    "category": "Object",
}

import os

from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty


class ViceCityIPLPreferences(AddonPreferences):
    bl_idname = __name__
    
    lFileName : bpy.props.StringProperty(name="FileName", default="Keksimus.ipl")
    lPath : bpy.props.StringProperty(name="Path", default="C:/Decimus/", subtype='FILE_PATH')

    def draw(self, context):
        layout = self.layout
        layout.label(text="You want to change dat:")
        layout.prop(self, "lFileName")
        layout.prop(self, "lPath")


class ViceCityIPLGenerator(bpy.types.Operator):
    """ViceCityIPLGenerator"""
    bl_idname = "object.vicecityiplgenerator"
    bl_label = "ViceCityIPLGenerator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        lOutputIPL = []
        lOutputIPL.append("inst");

        context = bpy.context

        lSelectedObjects = bpy.context.selected_objects
        for lObject in lSelectedObjects:    
            lData="";
            
            if("Id" in lObject):                
                lData += str(lObject["Id"]) + ", ";
            else:
                lData += "0, "

            if("ModelName" in lObject): 
                lData += str(lObject["ModelName"]) + ", ";
            else:
                lData += "ModelusKovalsonus, "

            if("Interior" in lObject):                
                lData += str(lObject["Interior"]) + ", ";
            else:
                lData += "0.0, "

            lData += str("%.7f" % lObject.location.x) + ", "\
            + str("%.7f" % lObject.location.y) + ", "\
            + str("%.7f" % lObject.location.z) + ", "\

            lData += "1.0, 1.0, 1.0, "

            lData += str("%.7f" % lObject.rotation_euler.to_quaternion().x) + ", "\
            + str("%.7f" % lObject.rotation_euler.to_quaternion().y) + ", "\
            + str("%.7f" % lObject.rotation_euler.to_quaternion().z) + ", "\
            + str("%.7f" % lObject.rotation_euler.to_quaternion().w)

            print(lOutputIPL)
            lOutputIPL.append(lData);

        lOutputIPL.append("end");
        print(lOutputIPL);
        
        lPath = str(context.preferences.addons[__name__].preferences.lPath)
        lFileName = str(context.preferences.addons[__name__].preferences.lFileName)

        # Ensure all folders of the path exist
        os.makedirs(lPath, exist_ok=True)

        # Fill ipls file
        with open(lPath + lFileName, "w") as file:
            file.write("\n".join(lOutputIPL))

        return{'FINISHED'}



# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ViceCityIPLGenerator)
    bpy.utils.register_class(ViceCityIPLPreferences)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(ViceCityIPLGenerator.bl_idname, 'NUMPAD_1', 'PRESS', ctrl=False, shift=True)
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(ViceCityIPLPreferences)
    bpy.utils.unregister_class(ViceCityIPLGenerator)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()