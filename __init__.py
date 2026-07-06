import bpy
import importlib
from .src.tools.SugarKeyconfigBuilder import BuildSugarKeyconfigOperator
from .src.tools import SugarKit
from .src.tools.SugarUtils import getClassesFromFileModule


bl_info = {
    "name": "Sugar Kit",
    "category": "Misc",
    "description": "QoL features.",
    "author": "xx",
    "version": (3, 1, 2),  # major version equals target Blender version
    "blender": (3, 6, 0),
}


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator(BuildSugarKeyconfigOperator.bl_idname,
                     text="Rebuild Sugar Hotkeys")


def register():
    bpy.utils.register_class(AddonPreferences)
    bpy.utils.register_class(BuildSugarKeyconfigOperator)

    for cls in getClassesFromFileModule(SugarKit):
        bpy.utils.register_class(cls)

    SugarKit.Props(True)
    SugarKit.Menus(True)
    SugarKit.Subscriptions(True)
    SugarKit.Hotkeys(True)

    importlib.reload(SugarKit)


def unregister():
    bpy.utils.unregister_class(BuildSugarKeyconfigOperator)
    bpy.utils.unregister_class(AddonPreferences)

    for cls in getClassesFromFileModule(SugarKit):
        bpy.utils.unregister_class(cls)

    SugarKit.Props(False)
    SugarKit.Menus(False)
    SugarKit.Subscriptions(False)
    SugarKit.Hotkeys(False)


if __name__ == "__main__":
    register()
