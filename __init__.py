import bpy
import importlib
from .Sugar_Keyconfig_Builder import BuildSugarKeyconfigOperator
from .src.tools.SugarKit_helpers import addAddonKeymapItem, removeAddonKeymapItems
from .src.tools import SugarKit
from .src.tools.SugarKit import *


bl_info = {
    "name": "Sugar Kit",
    "category": "Misc",
    "description": "QoL features.",
    "author": "nyamba",
    "version": (3, 1, 2),
    "blender": (3, 6, 0),
}


class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator(BuildSugarKeyconfigOperator.bl_idname,
                     text="Rebuild Sugar Keyconfig")


def register():
    # / Preferences
    bpy.utils.register_class(BuildSugarKeyconfigOperator)
    bpy.utils.register_class(AddonPreferences)

    # / SugarKit
    importlib.reload(SugarKit)
    SugarKit.Props(True)
    SugarKit.Menus(True)
    SugarKit.Subscriptions(True)
    # Windows Utils
    bpy.utils.register_class(WindowUpdateGlobalEventOperator)
    # Object Viewport Alpha/Color
    bpy.utils.register_class(ObjectViewportAlphaToggleOperator)
    addAddonKeymapItem('3D View', ObjectViewportAlphaToggleOperator.bl_idname,
                       'NINE')
    bpy.utils.register_class(ObjectViewportColorSetPanelOperator)
    bpy.utils.register_class(ObjectViewportColorSetPanel)
    addAddonKeymapItem('Object Mode', ObjectViewportColorSetPanelOperator.bl_idname,
                       'C')
    # Object Modifiers Setups
    bpy.utils.register_class(ModifierSetupAxisBendOperator)
    addAddonKeymapItem('Object Mode', ModifierSetupAxisBendOperator.bl_idname,
                       'B shift alt A')
    bpy.utils.register_class(ModifierSetupRadialArrayOperator)
    addAddonKeymapItem('Object Mode', ModifierSetupRadialArrayOperator.bl_idname,
                       'A shift alt R')
    # Outliner Unhide All Collections
    bpy.utils.register_class(OutlinerUnhideAllCollectionsOperator)
    for kmn in ['Object Mode', 'Outliner']:
        addAddonKeymapItem(kmn, OutlinerUnhideAllCollectionsOperator.bl_idname,
                           'H ctrl alt')
    # Outliner Select Grouped
    bpy.utils.register_class(OutlinerSelectGroupedOperator)
    addAddonKeymapItem('Outliner', OutlinerSelectGroupedOperator.bl_idname,
                       'G')
    bpy.utils.register_class(OutlinerSelectGroupedUnhideOperator)
    addAddonKeymapItem('Outliner', OutlinerSelectGroupedUnhideOperator.bl_idname,
                       'G DOUBLE_CLICK')
    # Vertex Groups Ops
    bpy.utils.register_class(VertexGroupRenamePanelOperator)
    bpy.utils.register_class(VertexGroupRenamePanel)
    addAddonKeymapItem('Mesh', VertexGroupRenamePanelOperator.bl_idname,
                       'R ctrl alt')
    bpy.utils.register_class(VertexGroupToSculptFaceSetOperator)
    addAddonKeymapItem('Sculpt', VertexGroupToSculptFaceSetOperator.bl_idname,
                       'G alt')
    bpy.utils.register_class(VertexGroupToPaintSelectMaskOperator)
    for kmn in ['Vertex Selection (Weight, Vertex)', 'Face Mask (Weight, Vertex, Texture)']:
        addAddonKeymapItem('Paint ' + kmn, VertexGroupToPaintSelectMaskOperator.bl_idname,
                           'G')
    # Curve Select Whole Handle
    bpy.utils.register_class(CurveSelectWholeHandlePointsOperator)
    addAddonKeymapItem('Curve', CurveSelectWholeHandlePointsOperator.bl_idname,
                       'LEFT_SHIFT DOUBLE_CLICK')
    # Curve Toggle Props
    bpy.utils.register_class(CurveToggleDepthOperator)
    addAddonKeymapItem('Curve', CurveToggleDepthOperator.bl_idname,
                       'T shift')
    bpy.utils.register_class(CurveToggleFillCapsOperator)
    addAddonKeymapItem('Curve', CurveToggleFillCapsOperator.bl_idname,
                       'F shift')
    # Brush Texture Image
    bpy.utils.register_class(BrushTextureImageSetMenuOperator)
    bpy.utils.register_class(BrushTextureImageSetMenu)
    for kmn in ["Sculpt", "Vertex Paint", "Weight Paint", "Image Paint"]:
        addAddonKeymapItem(kmn, BrushTextureImageSetMenuOperator.bl_idname,
                           'T ctrl')
    bpy.utils.register_class(BrushMaskTextureImageSetMenuOperator)
    bpy.utils.register_class(BrushMaskTextureImageSetMenu)
    addAddonKeymapItem('Image Paint', BrushMaskTextureImageSetMenuOperator.bl_idname,
                       'T alt')
    # Sculpt Draw Curve
    bpy.utils.register_class(SculptDrawCurveOperator)
    addAddonKeymapItem('Sculpt', SculptDrawCurveOperator.bl_idname,
                       'C shift alt')
    # Sculpt Trim Curve
    bpy.utils.register_class(SculptTrimCurveModalOperator)
    bpy.utils.register_class(SculptTrimCurveResolutionDialogOperator)
    addAddonKeymapItem('Sculpt', SculptTrimCurveModalOperator.bl_idname,
                       'X shift alt')
    # Sculpt Symmetrize Weld
    bpy.utils.register_class(SculptSymmetrizeWeldPanelOperator)
    bpy.utils.register_class(SculptSymmetrizeWeldPanel)
    addAddonKeymapItem('Sculpt', SculptSymmetrizeWeldPanelOperator.bl_idname,
                       'W shift alt')
    # Paint Gradient Settings
    bpy.utils.register_class(PaintGradientSettingsPanelOperator)
    bpy.utils.register_class(PaintGradientSettingsPanel)
    for km in ['Vertex Paint', 'Image Paint']:
        addAddonKeymapItem(km, PaintGradientSettingsPanelOperator.bl_idname,
                           'G ctrl')
    # Paint Color Palette
    bpy.utils.register_class(PaintColorPalettePanelOperator)
    bpy.utils.register_class(PaintColorPalettePanel)
    for km in ['Vertex Paint', 'Image Paint']:
        addAddonKeymapItem(km, PaintColorPalettePanelOperator.bl_idname,
                           'C')
    # Paint Mask
    bpy.utils.register_class(PaintMaskUvTransformProps)
    bpy.types.Object.sk_paint_mask_uv_transform = bpy.props.PointerProperty(
        type=PaintMaskUvTransformProps)
    bpy.utils.register_class(PaintMaskUvTransformPanelOperator)
    bpy.utils.register_class(PaintMaskUvTransformPanel)
    addAddonKeymapItem('Image Paint', PaintMaskUvTransformPanelOperator.bl_idname,
                       'Q ctrl')
    bpy.utils.register_class(PaintMaskImageInvertOperator)
    addAddonKeymapItem('Image Paint', PaintMaskImageInvertOperator.bl_idname,
                       'Q alt')
    # Pack All Saved
    bpy.utils.register_class(PackAllSavedOperator)
    addAddonKeymapItem('Window', PackAllSavedOperator.bl_idname,
                       'SPACE shift ctrl')
    # Image Pack/Unpack
    bpy.utils.register_class(ImagePackOperator)
    addAddonKeymapItem('Image', ImagePackOperator.bl_idname,
                       'SPACE alt')
    bpy.utils.register_class(ImageUnpackOperator)
    addAddonKeymapItem('Image', ImageUnpackOperator.bl_idname,
                       'SPACE alt DOUBLE_CLICK')
    # Image/Shading Create New
    bpy.utils.register_class(ShadingCreateNewOperator)
    addAddonKeymapItem('Node Editor', ShadingCreateNewOperator.bl_idname,
                       'N alt')
    # Image/Shading Set Active
    bpy.utils.register_class(ImageSetActiveMenuOperator)
    bpy.utils.register_class(ImageSetActiveMenu)
    addAddonKeymapItem('Image', ImageSetActiveMenuOperator.bl_idname,
                       'TAB shift ctrl')
    bpy.utils.register_class(ShadingSetActiveMenuOperator)
    bpy.utils.register_class(ShadingSetActiveMenu)
    addAddonKeymapItem('Node Editor', ShadingSetActiveMenuOperator.bl_idname,
                       'TAB shift ctrl')
    # Image/Shading Keep Fake User
    bpy.utils.register_class(ImageKeepFakeUserOperator)
    addAddonKeymapItem('Image', ImageKeepFakeUserOperator.bl_idname,
                       'K')
    bpy.utils.register_class(ShadingKeepFakeUserOperator)
    addAddonKeymapItem('Node Editor', ShadingKeepFakeUserOperator.bl_idname,
                       'K')
    # Image/Shading Make Single Copy
    bpy.utils.register_class(ImageMakeSingleCopyOperator)
    addAddonKeymapItem('Image', ImageMakeSingleCopyOperator.bl_idname,
                       'M alt')
    bpy.utils.register_class(MaterialMakeSingleCopyOperator)
    addAddonKeymapItem('Node Editor', MaterialMakeSingleCopyOperator.bl_idname,
                       'M alt')
    # Image/Shading Close
    bpy.utils.register_class(ImageCloseOperator)
    addAddonKeymapItem('Image', ImageCloseOperator.bl_idname,
                       'X ctrl alt')
    bpy.utils.register_class(ShadingCloseOperator)
    addAddonKeymapItem('Node Editor', ShadingCloseOperator.bl_idname,
                       'X ctrl alt')
    # Image/Shading Remove
    bpy.utils.register_class(ImageRemoveOperator)
    bpy.utils.register_class(ImageRemoveConfirmMenuOperator)
    bpy.utils.register_class(ImageRemoveConfirmMenu)
    addAddonKeymapItem('Image',
                       ImageRemoveOperator.bl_idname,
                       'X shift ctrl')
    bpy.utils.register_class(ShadingRemoveOperator)
    bpy.utils.register_class(ShadingRemoveConfirmMenuOperator)
    bpy.utils.register_class(ShadingRemoveConfirmMenu)
    addAddonKeymapItem('Node Editor',
                       ShadingRemoveOperator.bl_idname,
                       'X shift ctrl')


def unregister():
    # / Preferences
    bpy.utils.unregister_class(BuildSugarKeyconfigOperator)
    bpy.utils.unregister_class(AddonPreferences)
    # / SugarKit
    SugarKit.Props(False)
    SugarKit.Menus(False)
    SugarKit.Subscriptions(False)
    bpy.utils.unregister_class(WindowUpdateGlobalEventOperator)
    bpy.utils.unregister_class(ObjectViewportAlphaToggleOperator)
    bpy.utils.unregister_class(
        ObjectViewportColorSetPanelOperator)
    bpy.utils.unregister_class(ObjectViewportColorSetPanel)
    bpy.utils.unregister_class(ModifierSetupAxisBendOperator)
    bpy.utils.unregister_class(ModifierSetupRadialArrayOperator)
    bpy.utils.unregister_class(OutlinerUnhideAllCollectionsOperator)
    bpy.utils.unregister_class(OutlinerSelectGroupedOperator)
    bpy.utils.unregister_class(OutlinerSelectGroupedUnhideOperator)
    bpy.utils.unregister_class(VertexGroupRenamePanelOperator)
    bpy.utils.unregister_class(VertexGroupRenamePanel)
    bpy.utils.unregister_class(VertexGroupToSculptFaceSetOperator)
    bpy.utils.unregister_class(VertexGroupToPaintSelectMaskOperator)
    bpy.utils.unregister_class(CurveSelectWholeHandlePointsOperator)
    bpy.utils.unregister_class(CurveToggleDepthOperator)
    bpy.utils.unregister_class(CurveToggleFillCapsOperator)
    bpy.utils.unregister_class(BrushTextureImageSetMenuOperator)
    bpy.utils.unregister_class(BrushTextureImageSetMenu)
    bpy.utils.unregister_class(BrushMaskTextureImageSetMenuOperator)
    bpy.utils.unregister_class(BrushMaskTextureImageSetMenu)
    bpy.utils.unregister_class(SculptDrawCurveOperator)
    bpy.utils.unregister_class(SculptTrimCurveModalOperator)
    bpy.utils.unregister_class(SculptTrimCurveResolutionDialogOperator)
    bpy.utils.unregister_class(SculptSymmetrizeWeldPanelOperator)
    bpy.utils.unregister_class(SculptSymmetrizeWeldPanel)
    bpy.utils.unregister_class(PaintGradientSettingsPanelOperator)
    bpy.utils.unregister_class(PaintGradientSettingsPanel)
    bpy.utils.unregister_class(PaintColorPalettePanelOperator)
    bpy.utils.unregister_class(PaintColorPalettePanel)
    bpy.utils.unregister_class(PaintMaskUvTransformProps)
    del bpy.types.Object.sk_paint_mask_uv_transform
    bpy.utils.unregister_class(PaintMaskUvTransformPanelOperator)
    bpy.utils.unregister_class(PaintMaskUvTransformPanel)
    bpy.utils.unregister_class(PaintMaskImageInvertOperator)
    bpy.utils.unregister_class(PackAllSavedOperator)
    bpy.utils.unregister_class(ImagePackOperator)
    bpy.utils.unregister_class(ImageUnpackOperator)
    bpy.utils.unregister_class(ShadingCreateNewOperator)
    bpy.utils.unregister_class(ImageSetActiveMenuOperator)
    bpy.utils.unregister_class(ImageSetActiveMenu)
    bpy.utils.unregister_class(ShadingSetActiveMenuOperator)
    bpy.utils.unregister_class(ShadingSetActiveMenu)
    bpy.utils.unregister_class(ImageKeepFakeUserOperator)
    bpy.utils.unregister_class(ShadingKeepFakeUserOperator)
    bpy.utils.unregister_class(ImageMakeSingleCopyOperator)
    bpy.utils.unregister_class(MaterialMakeSingleCopyOperator)
    bpy.utils.unregister_class(ImageCloseOperator)
    bpy.utils.unregister_class(ShadingCloseOperator)
    bpy.utils.unregister_class(ImageRemoveOperator)
    bpy.utils.unregister_class(ImageRemoveConfirmMenuOperator)
    bpy.utils.unregister_class(ImageRemoveConfirmMenu)
    bpy.utils.unregister_class(ShadingRemoveOperator)
    bpy.utils.unregister_class(ShadingRemoveConfirmMenuOperator)
    bpy.utils.unregister_class(ShadingRemoveConfirmMenu)
    removeAddonKeymapItems()


if __name__ == "__main__":
    register()
