import bpy
from bpy.types import bpy_prop_collection
from bpy.app.handlers import persistent
from types import SimpleNamespace
import math
from .SugarUtils import *


def Props(isRegister):
    def handleActiveVertGroupNameUpdate(self, context):
        self.vertex_groups.active.name = self.xx_active_vert_group_name

    if isRegister:
        bpy.types.Object.xx_active_vert_group_name = bpy.props.StringProperty(
            name="", update=handleActiveVertGroupNameUpdate)
    else:
        del bpy.types.Object.xx_active_vert_group_name


def Menus(isRegister):
    def view3d_mt_view(self, context):
        self.layout.separator()
        self.layout.operator_context = "INVOKE_DEFAULT"
        self.layout.operator(ObjectViewportAlphaToggleOperator.bl_idname)

    if isRegister:
        bpy.types.VIEW3D_MT_view.append(view3d_mt_view)
    else:
        bpy.types.VIEW3D_MT_view.remove(view3d_mt_view)


def Subscriptions(isRegister):
    SubscribeBrushColor(isRegister)
    SubscribeWorkSpace(isRegister)


def Hotkeys(isRegister):
    if isRegister:
        # Object Viewport Display Props
        addAddonKeymapItem('Object Mode', ObjectViewportColorSetPanelOperator.bl_idname,
                           'C')
        addAddonKeymapItem('3D View', ObjectViewportAlphaToggleOperator.bl_idname,
                           'NINE')
        for kmn in ['Object Mode', 'Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Texture Paint']:
            addAddonKeymapItem(kmn, ObjectViewportAlphaToggleOperator.bl_idname,
                               'ACCENT_GRAVE Z')
        # Objects Collections Unable Visibility
        for kmn in ['Object Mode', 'Outliner']:
            addAddonKeymapItem(kmn, ObjectUnhideAllCollectionsButKeepObjectsHiddenOperator.bl_idname,
                               'H ctrl alt')
        # Object Modifier Setups
        addAddonKeymapItem('Object Mode', ObjectModifierSetupAxisBendOperator.bl_idname,
                           'LEFTMOUSE shift alt S')
        addAddonKeymapItem('Object Mode', ObjectModifierSetupRadialArrayOperator.bl_idname,
                           'LEFTMOUSE shift alt X')
        # Mesh Quad Fill
        addAddonKeymapItem('Mesh', MeshQuadFillOperator.bl_idname,
                           'Q ctrl')
        # Vertex Groups Ops
        addAddonKeymapItem('Mesh', VertexGroupRenamePanelOperator.bl_idname,
                           'R ctrl')
        for kmn in ['Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']:
            addAddonKeymapItem(kmn, VertexGroupSelectPanelOperator.bl_idname,
                               'G shift')
        addAddonKeymapItem('Sculpt', VertexGroupToSculptFaceSetOperator.bl_idname,
                           'G alt')
        for kmn in ['Vertex Selection (Weight, Vertex)', 'Face Mask (Weight, Vertex, Texture)']:
            addAddonKeymapItem('Paint ' + kmn, VertexGroupToPaintSelectMaskOperator.bl_idname,
                               'G')
        # Curve Select Whole Handle
        addAddonKeymapItem('Curve', CurveSelectWholeHandlePointsOperator.bl_idname,
                           'LEFTMOUSE shift DOUBLE_CLICK')
        # Curve Toggle Props
        addAddonKeymapItem('Curve', CurveToggleDepthOperator.bl_idname,
                           'T shift')
        addAddonKeymapItem('Curve', CurveToggleFillCapsOperator.bl_idname,
                           'F shift')
        # Curve Select Endpoints
        addAddonKeymapItem('Curve', CurveSelectEndpointsMenuOperator.bl_idname,
                           'E shift')
        # Sculpt Draw Curve
        addAddonKeymapItem('Sculpt', SculptDrawCurveOperator.bl_idname,
                           'C shift alt')
        # Sculpt Trim Curve
        addAddonKeymapItem('Sculpt', SculptTrimCurveModalOperator.bl_idname,
                           'X shift alt')
        # Sculpt Symmetrize Weld
        addAddonKeymapItem('Sculpt', SculptSymmetrizeWeldPanelOperator.bl_idname,
                           'W shift alt')
        # Sculpt Parts
        addAddonKeymapItem('Sculpt', SculptHoveredLoosePartSeparateOperator.bl_idname,
                           'RIGHTMOUSE ctrl CLICK')
        addAddonKeymapItem('Sculpt', SculptHoveredObjectJoinOperator.bl_idname,
                           'RIGHTMOUSE shift ctrl CLICK')
        addAddonKeymapItem('Sculpt', SculptRemeshByLoosePartsOperator.bl_idname,
                           'R shift ctrl')
        # Paint Gradient Settings
        for km in ['Vertex Paint', 'Image Paint']:
            addAddonKeymapItem(km, PaintGradientSettingsPanelOperator.bl_idname,
                               'G ctrl')
        # Paint Color Palette
        for km in ['Vertex Paint', 'Image Paint']:
            addAddonKeymapItem(km, PaintColorPalettePanelOperator.bl_idname,
                               'C')
        # Paint Mask
        addAddonKeymapItem('Image Paint', PaintMaskImageInvertOperator.bl_idname,
                           'Q alt')
        # Pack Image/All, Unpack Image
        addAddonKeymapItem('Image', ImagePackOperator.bl_idname,
                           'K ctrl')
        addAddonKeymapItem('Image', ImagePackOperator.bl_idname,
                           'LEFT_CTRL Z')
        addAddonKeymapItem('Window', PackAllSavedOperator.bl_idname,
                           'SPACE shift ctrl')
        addAddonKeymapItem('Image', ImageUnpackOperator.bl_idname,
                           'K alt')
        addAddonKeymapItem('Image', ImageUnpackOperator.bl_idname,
                           'LEFT_ALT Z')
        # Image/Shading Create New
        addAddonKeymapItem('Node Editor', ShadingCreateNewOperator.bl_idname,
                           'N alt')
        # Image/Shading Set Active
        addAddonKeymapItem('Image', ImageSetActiveMenuOperator.bl_idname,
                           'TAB shift ctrl')
        addAddonKeymapItem('Node Editor', ShadingSetActiveMenuOperator.bl_idname,
                           'TAB shift ctrl')
        # Image/Shading Keep Fake User
        addAddonKeymapItem('Image', ImageKeepFakeUserOperator.bl_idname,
                           'K')
        addAddonKeymapItem('Image', ImageKeepFakeUserOperator.bl_idname,
                           'Z CLICK')
        addAddonKeymapItem('Node Editor', ShadingKeepFakeUserOperator.bl_idname,
                           'K')
        addAddonKeymapItem('Node Editor', ShadingKeepFakeUserOperator.bl_idname,
                           'Z CLICK')
        # Image/Shading Make Single Copy
        addAddonKeymapItem('Image', ImageMakeSingleCopyOperator.bl_idname,
                           'C alt')
        addAddonKeymapItem('Image', ImageMakeSingleCopyOperator.bl_idname,
                           'TAB Z')
        addAddonKeymapItem('Node Editor', MaterialMakeSingleCopyOperator.bl_idname,
                           'C alt')
        addAddonKeymapItem('Node Editor', MaterialMakeSingleCopyOperator.bl_idname,
                           'TAB Z')
        # Image/Shading Close
        addAddonKeymapItem('Image', ImageCloseOperator.bl_idname,
                           'X ctrl alt')
        addAddonKeymapItem('Node Editor', ShadingCloseOperator.bl_idname,
                           'X ctrl alt')
        # Image/Shading Remove
        addAddonKeymapItem('Image', ImageRemoveOperator.bl_idname,
                           'X shift ctrl')
        addAddonKeymapItem('Node Editor', ShadingRemoveOperator.bl_idname,
                           'X shift ctrl')
    else:
        removeAddonKeymapItems()


# / Window Utils

glob = SimpleNamespace()
glob.event = SimpleNamespace()


class WindowUpdateGlobalEventOperator(bpy.types.Operator):
    bl_idname = "window.xx_update_global_event"
    bl_label = ""

    def invoke(self, context, event):
        global glob
        # New SimpleNamespace event from bpy_dict event
        glob.event = toSimpleNameSpace(event)
        return {'FINISHED'}


glob.event.mouse_prev_x = -1
glob.event.mouse_prev_y = -1


def yield_global_event(event=None):
    global glob
    if not event:
        # Call from bpy.msgbus.subscribe_rna
        bpy.ops.window.xx_update_global_event('INVOKE_REGION_WIN')
    else:
        # Call from bpy.type.Operator invoke
        glob.event = toSimpleNameSpace(event)
    return glob.event


# / Object Tools


# TODO: 3.2.x If initially context.scene.tool_settings.unified_paint_settings.use_unified_color=False, set True and set False again after SubscribeBrushColor is finished \
class ObjectViewportColorSetPanelOperator(bpy.types.Operator):
    # This operator inits values for ObjectViewportColorSetPanel
    """Set object's active material viewport display color."""
    bl_label = "Set Viewport Color"
    bl_idname = "object.xx_active_material_viewport_color_panel"
    bl_options = {'REGISTER', 'UNDO'}

    select_with_same_mat: bpy.props.BoolProperty(
        name='Select Other', description='Select other with same material', default=False)

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        ensureActMatForActObjectInContext(context)

        mR, mG, mB, mA = context.active_object.active_material.diffuse_color

        # Init panel picker with mat color
        context.scene.tool_settings.gpencil_paint.brush.color = (mR, mG, mB)

        try:
            paletteColors = context.scene.tool_settings.gpencil_paint.palette.colors
        except Exception as er:
            paletteColors = None

        # Init/unset panel palette with mat color
        if (paletteColors):
            unsetActive = True
            for paletteColor in paletteColors:
                pcR, pcG, pcB = paletteColor.color
                if (pcR == mR and pcG == mG and pcB == mB):
                    unsetActive = False
                    paletteColors.active = paletteColor
            if (unsetActive):
                paletteColors.active = None

        # Select only objects with active material
        if self.select_with_same_mat:
            bpy.ops.object.select_linked(extend=False, type='MATERIAL')

        # Activate unified color to fix layout.template_palette color add
        context.scene.tool_settings.unified_paint_settings.use_unified_color = True

        bpy.ops.wm.call_panel(
            name=ObjectViewportColorSetPanel.bl_idname)

        return {'FINISHED'}


class ObjectViewportColorSetPanel(bpy.types.Panel):
    # This panel's changes trigger SubscribeBrushColor
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Set Viewport Color"
    bl_idname = "xx_active_material_viewport_color_panel"
    bl_ui_units_x = 10  # width

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        paint = context.scene.tool_settings.gpencil_paint

        if context.object:
            col = layout.column()
            col.template_color_picker(paint.brush, "color", value_slider=True)

            sub_row = layout.row(align=True)
            sub_row.prop(paint.brush, "color", text="")

            row = layout.row(align=True)
            row.template_ID(paint, "palette", new="palette.new")

            if paint.palette:
                layout.template_palette(paint, "palette", color=True)


glob.prev_palette_color = None


def SubscribeBrushColor(isRegister=True):
    brushColorOwner = object()

    def setObjectViewportColorSet():
        global glob

        try:
            mat = bpy.context.active_object.active_material
        except Exception as er:
            mat = None
        try:
            unifiedPaintSettings = bpy.context.scene.tool_settings.unified_paint_settings
        except Exception as er:
            unifiedPaintSettings = None
        try:
            brush = bpy.context.scene.tool_settings.gpencil_paint.brush
        except Exception as er:
            brush = None
        try:
            paletteColor = bpy.context.scene.tool_settings.gpencil_paint.palette.colors.active.color
        except Exception as er:
            paletteColor = None

        global_event = yield_global_event()
        space = getSpaceUnderMouseFromContextEvent(
            bpy.context, global_event)

        if (bpy.context.mode != 'OBJECT' or space.type != 'VIEW_3D' or not mat):
            glob.prev_palette_color = paletteColor
            return

        def setObjectUsersOfMatWithColor(r, g, b):
            for obj in getObjectUsersOfMat(mat, bpy.data.objects):
                if not len(obj.data.color_attributes):
                    appendNewColorAttrForObject(
                        obj, 'Attribute')  # creates new color attr to show it in vertex color shading color mode \
                firstMat = list(obj.material_slots)[0].material
                if (firstMat == mat):
                    obj.color = (r, g, b, 1.0)

        if (paletteColor == glob.prev_palette_color):
            # Color changed by picker
            if (brush and brush.color):
                bcR, bcG, bcB = brush.color
                mat.diffuse_color = (bcR, bcG, bcB, 1.0)
                if (unifiedPaintSettings):
                    unifiedPaintSettings.color = (bcR, bcG, bcB)
                setObjectUsersOfMatWithColor(bcR, bcG, bcB)
        else:
            # Color changed by palette
            if (paletteColor):
                pcR, pcG, pcB = paletteColor
                mat.diffuse_color = (pcR, pcG, pcB, 1.0)
                if (brush):
                    brush.color = (pcR, pcG, pcB)
                setObjectUsersOfMatWithColor(pcR, pcG, pcB)

        glob.prev_palette_color = paletteColor

    def handleBrushColorChange():
        # After ObjectViewportColorSetPanel changes
        setObjectViewportColorSet()

    def subscribeBrushColor():
        bpy.msgbus.subscribe_rna(
            key=(bpy.types.Brush, 'color'),
            owner=brushColorOwner,
            args=(),
            notify=handleBrushColorChange,
            options={"PERSISTENT"}
        )

    @persistent
    def resubscribeBrushColor(dummy):
        subscribeBrushColor()

    def unsubscribeBrushColor():
        bpy.msgbus.clear_by_owner(brushColorOwner)

    if (isRegister):
        subscribeBrushColor()
        bpy.app.handlers.load_post.append(resubscribeBrushColor)
    else:
        unsubscribeBrushColor()


class ObjectViewportAlphaToggleOperator(bpy.types.Operator):
    """Toggle object's viewport display color alpha."""
    bl_label = "Toggle Opacity"
    bl_idname = "object.xx_object_toggle_viewport_alpha"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects and len(context.selected_objects)

    def execute(self, context):
        ensureActMatForActObjectInContext(context)

        actObjActMat = context.active_object.active_material
        r, g, b, alpha = actObjActMat.diffuse_color

        for obj in context.selected_objects:
            # Set object materials viewport alpha
            if not obj.material_slots or not len(obj.material_slots):
                appendNewActMatToObject(
                    obj, (1.0, 1.0, 1.0, 0.3 if alpha == 1.0 else 1.0))
            else:
                for ms in obj.material_slots:
                    mat = ms.material
                    mR, mG, mB, mA = mat.diffuse_color
                    mat.diffuse_color = (
                        mR, mG, mB, 0.3 if alpha == 1.0 else 1.0)
            # Set object viewport alpha
            if not hasattr(obj, 'color') or not obj.color:
                setattr(obj, 'color', (
                    1.0, 1.0, 1.0, 0.3 if alpha == 1.0 else 1.0))
            else:
                oR, oG, oB, oA = obj.color
                obj.color = (
                    oR, oG, oB, 0.3 if alpha == 1.0 else 1.0)

        return {'FINISHED'}


class ObjectUnhideAllCollectionsButKeepObjectsHiddenOperator(bpy.types.Operator):
    bl_label = "Unhide All Collections But Keep Objects Hidden"
    bl_idname = "object.xx_object_unhide_all_collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            collections = context.scene.view_layers[0].layer_collection.children
        except Exception as er:
            collections = None
        if not collections or not len(collections):
            return {'FINISHED'}
        for col in collections:
            col.hide_viewport = False
        return {'FINISHED'}


# Modifier Setups


class ObjectModifierSetupAxisBendOperator(bpy.types.Operator):
    bl_label = "Add Modifier Setup"
    bl_idname = "object.xx_modifier_setup_axis_bend"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        obj = context.active_object

        empty = bpy.data.objects.new(name="_bend_empty", object_data=None)
        col = getObjectCollection(obj)
        moveObjectToCollection(empty, col)
        empty.parent = obj
        # Justifies empty's rotation (in ui its done automatically)
        empty.scale = obj.scale

        modifier = obj.modifiers.new(
            name="Simple Deform", type='SIMPLE_DEFORM')
        modifier.deform_method = 'BEND'
        modifier.origin = empty

        obj.select_set(False)
        empty.select_set(True)
        bpy.context.view_layer.objects.active = empty

        return {'FINISHED'}


class ObjectModifierSetupRadialArrayOperator(bpy.types.Operator):
    bl_label = "Add Modifier Setup"
    bl_idname = "object.xx_setup_radial_array_modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def execute(self, context):
        obj = context.active_object
        applyObjectTransformsWithContext(context, obj, ['scale'])

        empty = bpy.data.objects.new(name="_radial_empty", object_data=None)
        col = getObjectCollection(obj)
        moveObjectToCollection(empty, col)
        empty.parent = obj

        modifier = obj.modifiers.new(
            name="Array", type='ARRAY')
        modifier.use_relative_offset = False
        modifier.use_object_offset = True
        modifier.offset_object = empty

        obj.select_set(False)
        empty.select_set(True)
        bpy.context.view_layer.objects.active = empty

        return {'FINISHED'}


# / Mesh Tools


class MeshQuadFillOperator(bpy.types.Operator):
    bl_label = "Mesh Quad Fill"
    bl_idname = "mesh.xx_mesh_quad_fill"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.mesh.tris_convert_to_quads(
            face_threshold=1.5708,  shape_threshold=1.5708)  # Face/Shape Angle:[90deg] \
        return {'FINISHED'}


# TODO: 3.2.x InterceptiveMerge (alt C)
#
# - create vertex group from selected (1 for intersect)
# - select more (face step [_])
# - create vertex group from selected (2 for merge)
# - deselect all, select group 1
# - knife intersect
# - select group 2
# - merge by distance
# - remove group 2
# - deselect all, select group 1
# - remove group 1


# / Vertex Groups Tools


class VertexGroupRenamePanelOperator(bpy.types.Operator):
    bl_label = "Vertex Group Rename"
    bl_idname = "mesh.xx_vertex_group_rename"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            actVertGroup = context.active_object.vertex_groups.active
        except Exception as er:
            actVertGroup = None
        return actVertGroup

    def execute(self, context):
        vertGroupName = context.active_object.vertex_groups.active.name
        context.active_object.xx_active_vert_group_name = vertGroupName

        bpy.ops.wm.call_panel(
            name=VertexGroupRenamePanel.bl_idname, keep_open=False)

        return {'FINISHED'}


def row_with_icon(layout, icon):
    row = layout.row()
    row.activate_init = True
    row.label(icon=icon)
    return row


class VertexGroupRenamePanel(bpy.types.Panel):
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Rename Active Vertex Group"
    bl_idname = 'TOPBAR_PT_name_active_vertex_group'
    bl_ui_units_x = 14

    def draw(self, context):
        found = False

        if context.mode == 'EDIT_MESH':
            self.layout.label(text="Vertex Group Name")
            target = context.active_object
            if target:
                row = row_with_icon(self.layout, 'MESH_DATA')
                row.prop(target, "xx_active_vert_group_name", text="")
                found = True

        if not found:
            row = row_with_icon(self.layout, 'ERROR')
            row.label(text="No active vertex group")


class VertexGroupSelectPanelOperator(bpy.types.Operator):
    bl_label = "Vertex Group Select"
    bl_idname = "mesh.xx_vertex_group_select"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            vertGroups = context.active_object.vertex_groups
        except Exception as er:
            vertGroups = None
        return vertGroups and len(vertGroups)

    def execute(self, context):
        bpy.ops.wm.call_panel(
            name=VertexGroupSelectPanel.bl_idname, keep_open=True)
        return {'FINISHED'}


class VertexGroupSelectPanel(bpy.types.Panel):
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Active Vertex Group"
    bl_idname = "xx_vertex_group_select"
    bl_ui_units_x = 8  # width

    def draw(self, context):
        layout = self.layout
        ob = context.object
        row = layout.row()
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups",
                          ob.vertex_groups, "active_index", rows=len(ob.vertex_groups) if len(ob.vertex_groups) < 21 else 21)


class VertexGroupToSculptFaceSetOperator(bpy.types.Operator):
    bl_label = "Vertex Group To Sculpt Face Set"
    bl_idname = "paint.xx_vertex_group_to_sculpt_face_set"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            actVertGroup = context.active_object.vertex_groups.active
        except Exception as er:
            actVertGroup = None
        return actVertGroup

    def execute(self, context):
        mode = getObjectModeFromContext(context)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.mode_set(mode=mode)
        bpy.ops.sculpt.face_sets_create(mode='SELECTION')
        return {'FINISHED'}


class VertexGroupToPaintSelectMaskOperator(bpy.types.Operator):
    bl_label = "Vertex Group To Paint Select Mask"
    bl_idname = "paint.xx_vertex_group_to_paint_select_mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            actVertGroup = context.active_object.vertex_groups.active
        except Exception as er:
            actVertGroup = None
        return actVertGroup

    def execute(self, context):
        mode = getObjectModeFromContext(context)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.mode_set(mode=mode)
        return {'FINISHED'}


# / Curve Tools


class CurveSelectWholeHandlePointsOperator(bpy.types.Operator):
    bl_label = "Curve Select Whole Handle Points"
    bl_idname = "curve.xx_curve_select_whole_handle_points"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        actPoint = getCurveActivePoint(context.active_object, True)
        selectWholeBezierPoint(actPoint)
        return {'FINISHED'}


class CurveToggleDepthOperator(bpy.types.Operator):
    bl_label = "Curve Toggle Depth"
    bl_idname = "curve.xx_curve_toggle_depth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            curveData = context.active_object.data
        except Exception as er:
            curveData = None
        return curveData and context.active_object.type == "CURVE"

    def execute(self, context):
        curveData = context.active_object.data
        curveData.bevel_depth = 0.01 if curveData.bevel_depth == 0.0 else 0.0
        return {'FINISHED'}


class CurveToggleFillCapsOperator(bpy.types.Operator):
    bl_label = "Curve Toggle Fill Caps"
    bl_idname = "curve.xx_curve_toggle_fill_caps"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            curveData = context.active_object.data
        except Exception as er:
            curveData = None
        return curveData and context.active_object.type == "CURVE"

    def execute(self, context):
        curveData = context.active_object.data
        curveData.use_fill_caps = True if curveData.use_fill_caps == False else False
        return {'FINISHED'}


class CurveSelectEndpointsMenuOperator(bpy.types.Operator):
    bl_label = "Curve Select Endpoints Menu"
    bl_idname = "curve.xx_curve_select_endpoints_menu"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_menu(
            name=CurveSelectEndpointsMenu.bl_idname)
        return {'FINISHED'}


class CurveSelectEndpointsMenu(bpy.types.Menu):
    bl_label = "Select Endpoints"
    bl_idname = "xx_curve_select_endpoints_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        opStart = layout.operator(
            CurveSelectEndpointsOperator.bl_idname, text="Start")
        opStart.type = 'START'
        opEnd = layout.operator(
            CurveSelectEndpointsOperator.bl_idname, text="End")
        opEnd.type = 'END'


class CurveSelectEndpointsOperator(bpy.types.Operator):
    bl_label = "Curve Select Endpoints"
    bl_idname = "curve.xx_curve_select_endpoints"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.EnumProperty(name='Type', items=[
        ('START', 'Start', ''), ('END', 'End', '')])
    extend: bpy.props.BoolProperty(name='Extend', default=True)
    step: bpy.props.IntProperty(name='Step', default=0, min=0)

    def execute(self, context):
        curve = context.active_object

        if not self.extend:
            bpy.ops.curve.select_all(action='DESELECT')

        for spline in curve.data.splines:
            targetIdx = 0 if self.type == 'START' else (
                len(spline.bezier_points) - 1)
            step = self.step if abs(self.step) < len(
                spline.bezier_points) else len(spline.bezier_points) - 1
            directedStep = step if self.type == 'START' else -1 * step
            spline.bezier_points[targetIdx +
                                 directedStep].select_control_point = True
            spline.bezier_points[targetIdx +
                                 directedStep].select_left_handle = True
            spline.bezier_points[targetIdx +
                                 directedStep].select_right_handle = True

        return {'FINISHED'}


# / Sculpt Tools


class SculptDrawCurveOperator(bpy.types.Operator):
    bl_label = "Sculpt Quick Draw Curve"
    bl_idname = "sculpt.xx_sculpt_draw_curve"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def invoke(self, context, event):
        context.tool_settings.curve_paint_settings.curve_type = 'BEZIER'
        context.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
        return self.execute(context)

    def execute(self, context):
        act = context.active_object
        drawCurve = createCurveAndEditInContext(context, 'DrawCurve')
        drawCurve.data.bevel_depth = 0.01
        drawCurve.data.use_fill_caps = True
        col = getObjectCollection(act)
        moveObjectToCollection(drawCurve, col)
        drawCurve.parent = act
        return {'FINISHED'}


# TODO: 3.2.x Make TRIM_CURVE_RESOLUTION setable as modal option
# TODO: 3.2.x Make modal keys setable from keymap settings
class SculptTrimCurveModalOperator(bpy.types.Operator):
    credits = [
        'https://blenderartists.org/t/how-can-i-ask-the-user-to-draw-a-curve/1462361',
        'https://blenderartists.org/t/using-grease-pencil-annotation-from-modal-in-blender-2-8/1203973',
        "https://www.youtube.com/watch?v=3C6wVPVrPtM",
    ]
    bl_idname = "sculpt.xx_trim_curve_modal"
    bl_label = "Sculpt Trim Curve Modal"
    bl_options = {"REGISTER", "UNDO"}

    DRAW_HEADER_TEXT = "Draw Trim Curve"
    DRAW_STATUS_TEXT = " ".join([
        "Cancel: Esc |",
        "Pass: Ent/Space |",
        "Draw: LM"
    ])
    HEADER_TEXT = "Trim Curve Interior (Toggle: T)"
    EXTERIOR_HEADER_TEXT = "Trim Curve Exterior (Toggle: T)"
    STATUS_TEXT = " ".join([
        "Cancel: Esc |",
        "Confirm: Ent/Space |",
        "Select/Move, Extend, Path, Whole: LM, Shift+LM, Ctrl+Dbl+LM, Shift+Dbl+LM |",
        "Select Whole, Path: Shift+Dbl+LM, Ctrl+Dbl+LM |",
        "Extrude/Insert/Close: Ctrl+LM |",
        "Delete: Alt+LM |",
        "Move, Scale, Rotate: RM, Shift+RM, Alt+RM |",
        "All, Invert: A, Alt+A |",
        "Vector/Auto, Toggle: shift 1/2, Dbl+Alt/LM |",
        "Recalc: Ctrl+R |",
        "Smooth: Shift+Alt+S |",
        "Undo, Redo: Ctrl+Z, Shift+Ctrl+Z",
    ])

    view_3d_space = bpy.props.PointerProperty(type=bpy.types.SpaceView3D)
    init_workspace = bpy.props.PointerProperty(type=bpy.types.WorkSpace)
    target_obj = bpy.props.PointerProperty(type=bpy.types.Object)
    trim_curve = bpy.props.PointerProperty(type=bpy.types.Curve)

    disabled_draw_keymap_items_ids = []
    disabled_pen_keymap_items_ids = []
    has_enabled_back_draw_keymap_items = False
    has_enabled_back_pen_keymap_items = False

    history_steps = 0
    dbl = {}

    is_init_orthographic = False
    is_draw = True
    is_exterior = False
    has_entered_in_between_tools = False
    has_chandes_header_by_submodal = False
    was_middle_pressed = False

    @classmethod
    def poll(cls, context):
        return context.active_object

    def invoke(self, context, event):
        self.initClassProps(self, context, event)
        self.mapModalKeys(self, context, True)

        context.window_manager.modal_handler_add(self)  # required for modal

        setModalTextInContext(
            context, self.DRAW_HEADER_TEXT, self.DRAW_STATUS_TEXT)

        context.tool_settings.curve_paint_settings.curve_type = 'BEZIER'
        context.tool_settings.curve_paint_settings.depth_mode = 'CURSOR'
        context.tool_settings.use_proportional_edit = False

        return {'RUNNING_MODAL'}

    @classmethod
    def initClassProps(cls, self, context, event):
        self.view_3d_space = getSpaceUnderMouseFromContextEvent(context, event)
        self.is_init_orthographic = self.view_3d_space.region_3d.is_orthographic_side_view
        self.init_workspace = findBpyObjectByName(
            context.window.workspace.name, bpy.data.workspaces)

        self.target_obj = findBpyObjectByName(context.active_object.name)

        self.trim_curve = createCurveAndEditInContext(
            context, 'TrimCurve', inFront=True)
        col = getObjectCollection(self.target_obj)
        moveObjectToCollection(self.trim_curve, col)
        self.trim_curve.parent = self.target_obj

    @classmethod
    def mapModalKeys(cls, self, context, doSet):
        drawKeymap = getKeymapFromContext(
            context, '3D View Tool: Edit Curve, Draw', 'user')
        penKeymap = getKeymapFromContext(
            context, '3D View Tool: Edit Curve, Curve Pen', 'user')

        if doSet:
            self.disableOldModalKeys(self, drawKeymap, penKeymap)
            self.appendNewModalKeys(drawKeymap, penKeymap)
        else:
            self.removeNewModalKeys(self, drawKeymap, penKeymap)
            self.unableOldModalKeys(self, drawKeymap, penKeymap)

    @classmethod
    def disableOldModalKeys(cls, self, drawKeymap, penKeymap):
        self.disabled_draw_keymap_items_ids = disableActiveKeymapItems(
            drawKeymap)
        self.disabled_pen_keymap_items_ids = disableActiveKeymapItems(
            penKeymap)

    @classmethod
    def removeNewModalKeys(cls, self, drawKeymap, penKeymap):
        if not self.has_enabled_back_draw_keymap_items:
            removeActiveKeymapItems(drawKeymap)
            self.has_enabled_back_draw_keymap_items = True
        if not self.has_enabled_back_pen_keymap_items:
            removeActiveKeymapItems(penKeymap)
            self.has_enabled_back_pen_keymap_items = True

    @classmethod
    def unableOldModalKeys(cls, self, drawKeymap, penKeymap):
        unableDisabledKeymapItems(
            drawKeymap, self.disabled_draw_keymap_items_ids)
        unableDisabledKeymapItems(
            penKeymap, self.disabled_pen_keymap_items_ids)

    @classmethod
    def appendNewModalKeys(cls, drawKeymap, penKeymap):
        # Draw
        addUserKeymapItem(drawKeymap, {'curve.draw': {'wait_for_input': False}},
                          'LEFTMOUSE')

        # Select/Move, Extend
        addUserKeymapItem(penKeymap, {'curve.pen': {'select_point': True, 'move_point': True, 'move_point': True, 'move_segment': True}},
                          'LEFTMOUSE')
        addUserKeymapItem(penKeymap, {'curve.pen': {'extend': True}},
                          'LEFTMOUSE shift')
        # Extrude, Insert, Close
        addUserKeymapItem(penKeymap, {'curve.pen': {'extrude_point': True, 'insert_point': True, 'close_spline': True, 'close_spline_method': 1}},
                          'LEFTMOUSE ctrl')
        # Delete
        addUserKeymapItem(penKeymap, {'curve.pen': {'delete_point': True}},
                          'LEFTMOUSE alt')
        # Toggle Type
        addUserKeymapItem(penKeymap, {'curve.pen': {'toggle_vector': True, 'cycle_handle_type': True}},
                          'LEFTMOUSE DOUBLE_CLICK')

    def modal(self, context, event):
        # PASS_THROUGH - execute modal defined operator and restart loop
        # RUNNING_MODAL - direct call operator and restart loop
        try:
            #: If/elif fold level: 4
            # C(event.type, ": ", event.value)

            global glob
            isPen = not self.is_draw
            isInBetweenTools = True if self.has_entered_in_between_tools else False
            self.has_entered_in_between_tools = False

            if (self.has_chandes_header_by_submodal):
                setModalTextInContext(
                    context, self.HEADER_TEXT if not self.is_exterior else self.EXTERIOR_HEADER_TEXT, self.STATUS_TEXT)
                self.has_chandes_header_by_submodal = False

            # / FINISH
            if eventKeyIs(event, 'RET') or eventKeyIs(event, 'SPACE'):
                if isPen:
                    self.finish(self, context)
                else:
                    setModalTextInContext(
                        context, self.HEADER_TEXT, self.STATUS_TEXT)
                    bpy.ops.wm.tool_set_by_id(name='builtin.pen')
                    self.is_draw = False
                return {'RUNNING_MODAL'}

            # / CANCEL
            elif eventKeyIs(event, 'ESC'):
                setActiveObjectInContext(
                    context, self.target_obj, mode='SCULPT', delPrev=True)
                setModalTextInContext(context, None)
                self.mapModalKeys(self, context, False)
                return {'CANCELLED'}
            # Workspace has changed
            elif event.value == 'PRESS' and self.init_workspace.name != context.window.workspace.name:
                setModalTextInContext(context, None)
                self.mapModalKeys(self, context, False)
                return {'CANCELLED'}
            # Tool has changed from ui
            elif not isInBetweenTools and ((self.is_draw and glob.workspace_active_tool_name != 'builtin.draw') or (isPen and glob.workspace_active_tool_name != 'builtin.pen')):
                setModalTextInContext(context, None)
                self.mapModalKeys(self, context, False)
                return {'CANCELLED'}

            # / PASS MODAL OPS
            # Draw start/end
            elif self.is_draw and (eventKeyIs(event, 'LEFTMOUSE') or eventKeyIs(event, 'LEFTMOUSE CLICK_DRAG')):
                return {'PASS_THROUGH'}
            elif self.is_draw and len(getCurvePointsAll(context.active_object)):
                setModalTextInContext(
                    context, self.HEADER_TEXT, self.STATUS_TEXT)
                bpy.ops.wm.tool_set_by_id(name='builtin.pen')
                self.is_draw = False
                self.has_entered_in_between_tools = True
                return {'PASS_THROUGH'}

            # Select/Move, Extend
            elif isPen and eventKeyIs(event, 'LEFTMOUSE') and not self.dbl.get('LEFTMOUSE'):
                self.history_steps += 1
                return {'PASS_THROUGH'}
            elif isPen and eventKeyIs(event, 'LEFTMOUSE shift') and not self.dbl.get('LEFTMOUSE shift'):
                self.history_steps += 1
                return {'PASS_THROUGH'}
            # Extrude, Insert, Close
            elif isPen and eventKeyIs(event, 'LEFTMOUSE ctrl') and not self.dbl.get('LEFTMOUSE ctrl'):
                curve = context.active_object

                # Skip if curve is empty
                if not curve.data.splines or not len(curve.data.splines):
                    return {'PASS_THROUGH'}

                # Return if curve is closed
                if isCurveMainSplineClosed(curve):
                    self.report({'INFO'}, "Open curve spline to extrude!")
                    return {'RUNNING_MODAL'}

                # Add point only to existing spline
                actPoint = getCurveActivePoint(curve)
                points = curve.data.splines[0].bezier_points
                if not actPoint or actPoint != points[0]:
                    curve.data.splines[0].bezier_points[len(
                        points) - 1].select_control_point = True

                self.history_steps += 1
                return {'PASS_THROUGH'}
            # Delete
            elif isPen and eventKeyIs(event, 'LEFTMOUSE alt'):
                self.history_steps += 1
                return {'PASS_THROUGH'}
            # Toggle Type
            elif isPen and eventKeyIs(event, 'LEFTMOUSE') and 'DBL':
                if not self.dbl.get('LEFTMOUSE'):
                    self.dbl['LEFTMOUSE'] = addTimerForContext(context)
                    return {'RUNNING_MODAL'}
                else:
                    self.dbl['LEFTMOUSE'] = removeTimerFromContext(
                        context, self.dbl.get('LEFTMOUSE'))

                self.history_steps += 1
                return {'PASS_THROUGH'}

            # / RUN OPS
            # Toggle Interior/exterior
            elif isPen and eventKeyIs(event, 'T'):
                self.is_exterior = not self.is_exterior
                setModalTextInContext(
                    context, self.HEADER_TEXT if not self.is_exterior else self.EXTERIOR_HEADER_TEXT, self.STATUS_TEXT)
                return {'RUNNING_MODAL'}

            # Extrude
            elif isPen and eventKeyIs(event, 'E'):
                curve = context.active_object
                # Return if curve is closed
                if isCurveMainSplineClosed(curve):
                    self.report({'INFO'}, "Open curve spline to extrude!")
                    return {'RUNNING_MODAL'}

                bpy.ops.curve.extrude_move('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}
            # Close
            elif isPen and eventKeyIs(event, 'C shift'):
                bpy.ops.curve.cyclic_toggle()
                return {'RUNNING_MODAL'}
            # Delete
            elif isPen and eventKeyIs(event, 'X ctrl'):
                self.history_steps += 1
                bpy.ops.curve.dissolve_verts()
                return {'RUNNING_MODAL'}

            # Move, Scale, Rotate
            elif isPen and eventKeyIs(event, 'RIGHTMOUSE'):
                bpy.ops.transform.translate('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'RIGHTMOUSE shift'):
                bpy.ops.transform.resize('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'RIGHTMOUSE alt'):
                bpy.ops.transform.rotate('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'D'):
                bpy.ops.transform.translate('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'S'):
                bpy.ops.transform.resize('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'R'):
                bpy.ops.transform.rotate('INVOKE_DEFAULT')
                self.has_chandes_header_by_submodal = True
                return {'RUNNING_MODAL'}

            # All, Invert
            elif isPen and eventKeyIs(event, 'A'):
                if getCurveActivePoint(context.active_object):
                    bpy.ops.curve.select_all(action='DESELECT')
                else:
                    bpy.ops.curve.select_all(action='SELECT')
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'A alt'):
                bpy.ops.curve.select_all(action='INVERT')
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            # Select Whole, Path
            elif isPen and eventKeyIs(event, 'LEFTMOUSE shift') and 'DBL':
                if not self.dbl.get('LEFTMOUSE shift'):
                    self.dbl['LEFTMOUSE shift'] = addTimerForContext(context)
                    return {'RUNNING_MODAL'}
                else:
                    self.dbl['LEFTMOUSE shift'] = removeTimerFromContext(
                        context, self.dbl.get('LEFTMOUSE shift'))

                actPoint = getCurveActivePoint(context.active_object, True)
                selectWholeBezierPoint(actPoint)
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'LEFTMOUSE ctrl') and 'DBL':
                if not self.dbl.get('LEFTMOUSE ctrl'):
                    self.dbl['LEFTMOUSE ctrl'] = addTimerForContext(context)
                    return {'RUNNING_MODAL'}
                else:
                    self.dbl['LEFTMOUSE ctrl'] = removeTimerFromContext(
                        context, self.dbl.get('LEFTMOUSE ctrl'))

                bpy.ops.curve.shortest_path_pick()
                self.history_steps += 1
                return {'RUNNING_MODAL'}

            # Vector, Auto, Toggle
            elif isPen and eventKeyIs(event, 'ONE shift'):
                bpy.ops.curve.handle_type_set(type='VECTOR')
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'TWO shift'):
                bpy.ops.curve.handle_type_set(type='AUTOMATIC')
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'LEFT_ALT') and 'DBL':
                if not self.dbl.get('ALT'):
                    self.dbl['ALT'] = addTimerForContext(context)
                    return {'RUNNING_MODAL'}
                else:
                    self.dbl['ALT'] = removeTimerFromContext(
                        context, self.dbl.get('ALT'))

                actPoint = getCurveActivePoint(context.active_object)
                if actPoint and actPoint.handle_left_type in ['FREE', 'VECTOR']:
                    bpy.ops.curve.handle_type_set(type='ALIGNED')
                else:
                    bpy.ops.curve.handle_type_set(type='FREE_ALIGN')
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            # Recalc handler
            elif isPen and eventKeyIs(event, 'R ctrl'):
                bpy.ops.curve.normals_make_consistent()
                self.history_steps += 1
                return {'RUNNING_MODAL'}
            # Smooth
            elif isPen and eventKeyIs(event, 'S shift alt'):
                bpy.ops.curve.smooth()
                self.history_steps += 1
                return {'RUNNING_MODAL'}

            # Undo, Redo
            elif isPen and eventKeyIs(event, 'Z ctrl') and self.history_steps > 0:
                self.history_steps -= 1
                bpy.ops.ed.undo()
                return {'RUNNING_MODAL'}
            elif isPen and eventKeyIs(event, 'Z shift ctrl'):
                try:
                    bpy.ops.ed.redo()
                    self.history_steps += 1
                except Exception as er:
                    pass
                return {'RUNNING_MODAL'}

            # / RUN OPS BLOCK
            # Remove timers (for dbl)
            if event.type == 'TIMER':
                for key in self.dbl.keys():
                    self.dbl[key] = removeTimerFromContext(
                        context, self.dbl.get(key))
                return {'RUNNING_MODAL'}
            # Restore modal text after other modal commands
            elif event.type in ['INBETWEEN_MOUSEMOVE', 'NONE']:
                if self.is_draw:
                    setModalTextInContext(
                        context, self.DRAW_HEADER_TEXT, self.DRAW_STATUS_TEXT)
                else:
                    setModalTextInContext(
                        context, self.HEADER_TEXT if not self.is_exterior else self.EXTERIOR_HEADER_TEXT, self.STATUS_TEXT)
                    bpy.ops.wm.tool_set_by_id(name='builtin.pen')
                self.has_entered_in_between_tools = True
                return {'RUNNING_MODAL'}
            # Block viewport navigation
            elif (
                event.type in ['MOUSEROTATE', 'MIDDLEMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM'] or
                event.value in ['PRESS', 'RELEASE', 'CLICK']
            ):
                # Fixes ortograthic view bug
                if self.is_init_orthographic and self.is_init_orthographic != self.view_3d_space.region_3d.is_orthographic_side_view:
                    bpy.ops.view3d.view_persportho()
                    self.view_3d_space.region_3d.is_orthographic_side_view = self.is_init_orthographic
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}

        except Exception as er:
            self.report({'ERROR'}, "{0}".format(er))
            setModalTextInContext(context, None)
            self.mapModalKeys(self, context, False)
            return {'CANCELLED'}

    @classmethod
    def finish(cls, self, context):
        try:
            TRIM_CURVE_RESOLUTION = 16

            # Close and convert curve to mesh
            setCurveCyclic(self.trim_curve, True)
            self.trim_curve.data.resolution_u = TRIM_CURVE_RESOLUTION
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

            # / Trim
            if not self.is_init_orthographic:
                # Prepare camera to perspective mesh transform
                bpy.ops.object.camera_add(align='VIEW')
                context.scene.camera = context.active_object
                bpy.ops.view3d.camera_to_view()
                bpy.ops.view3d.snap_cursor_to_selected()
                prevPivotPoint = str(
                    context.scene.tool_settings.transform_pivot_point)
                context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                # Fill mesh
                setActiveObjectInContext(
                    context, self.trim_curve, mode='EDIT', delPrev=True)
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.duplicate_move()
                viewport = self.view_3d_space.region_3d
                scaleAbs = math.ceil(viewport.view_distance * 2) * \
                    20  # VIEW_DISTANCE * BOTH_SIDES * BIG_NUMBER_TO_SURE_COVER_WHOLE_MESH \
                bpy.ops.transform.resize(
                    value=(scaleAbs, scaleAbs, scaleAbs))
                bpy.ops.mesh.select_all(action='INVERT')
                bpy.ops.mesh.duplicate_move()
                digitAbs = pow(10, len(str(scaleAbs)) + 1)
                bpy.ops.transform.resize(
                    value=(scaleAbs/digitAbs, scaleAbs/digitAbs, scaleAbs/digitAbs))
                context.scene.tool_settings.transform_pivot_point = prevPivotPoint
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bridge_edge_loops()
                bpy.ops.mesh.region_to_loop()
                bpy.ops.mesh.edge_face_add()
            else:
                # Fill mesh
                bpy.ops.object.editmode_toggle()  # EDIT
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.edge_face_add()
                bpy.ops.object.editmode_toggle()  # OBJECT
                solidifyMod = self.trim_curve.modifiers.new(
                    'TrimSolidify' + str(id(self.trim_curve)), 'SOLIDIFY')
                viewport = self.view_3d_space.region_3d
                thicknessAbs = math.ceil(
                    viewport.view_distance * 2) * 20  # VIEW_DISTANCE * BOTH_SIDES * BIG_NUMBER_TO_SURE_COVER_WHOLE_MESH \
                solidifyMod.thickness = thicknessAbs
                solidifyMod.offset = 0.0
                # Apply mod (for active)
                bpy.ops.object.modifier_apply(
                    modifier=solidifyMod.name)
            # Boolean opration
            setActiveObjectInContext(context, self.target_obj, mode='OBJECT')
            boolMod = self.target_obj.modifiers.new(
                'TrimBool' + str(id(self.target_obj)), 'BOOLEAN')
            moveObjectModifierAtTheEnd(self.target_obj, boolMod)
            boolMod.operation = 'DIFFERENCE' if not self.is_exterior else 'INTERSECT'
            boolMod.object = self.trim_curve
            boolMod.use_hole_tolerant = True
            # Apply mod (for active)
            bpy.ops.object.modifier_apply(
                modifier=boolMod.name)
            # Restore context
            setActiveObjectInContext(context, self.trim_curve)
            # self.trim_curve.display_type = 'WIRE'
            setActiveObjectInContext(
                context, self.target_obj, mode='SCULPT', delPrev=True)
            setModalTextInContext(context, None)
            self.mapModalKeys(self, context, False)

            return {'FINISHED'}

        except Exception as er:
            self.report({'ERROR'}, "{0}".format(er))
            setModalTextInContext(context, None)
            self.mapModalKeys(self, context, False)
            return {'CANCELLED'}


glob.workspace_active_tool_name = ''
glob.prev_workspace = None
glob.act_workspace = None


def SubscribeWorkSpace(isRegister=True):
    workSpaceOwner = object()

    def handleWorkSpaceChange():
        global glob

        try:
            glob.workspace_active_tool_name = bpy.context.workspace.tools.from_space_view3d_mode(
                bpy.context.mode, create=False).idname
        except Exception as er:
            glob.workspace_active_tool_name = ''
        try:
            glob.prev_workspace = findBpyObjectByName(
                glob.act_workspace.name, bpy.data.workspaces)
        except Exception as er:
            glob.prev_workspace = None
        try:
            glob.act_workspace = findBpyObjectByName(
                bpy.context.workspace.name, bpy.data.workspaces)
        except Exception as er:
            glob.act_workspace = None
        # Reset status text on checkout (clears unfinished modal text)
        try:
            if glob.prev_workspace.name != glob.act_workspace.name:
                bpy.context.workspace.status_text_set(None)
        except Exception as er:
            pass

    def subscribeWorkSpace():
        subscribeTo = (bpy.types.WorkSpace, 'tools')
        bpy.msgbus.subscribe_rna(
            key=subscribeTo,
            owner=workSpaceOwner,
            args=(),
            notify=handleWorkSpaceChange,
            options={'PERSISTENT'}
        )

    @persistent
    def resubscribeWorkSpace(dummy):
        subscribeWorkSpace()

    def unsubscribeWorkSpace():
        bpy.msgbus.clear_by_owner(workSpaceOwner)

    if (isRegister):
        subscribeWorkSpace()
        bpy.app.handlers.load_post.append(resubscribeWorkSpace)
    else:
        unsubscribeWorkSpace()


class SculptSymmetrizeWeldPanelOperator(bpy.types.Operator):
    bl_label = "Sculpt Symmetrize Weld Panel"
    bl_idname = "paint.xx_sculpt_symmetrize_weld_panel"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_panel(
            name=SculptSymmetrizeWeldPanel.bl_idname, keep_open=True)
        return {'FINISHED'}


class SculptSymmetrizeWeldPanel(bpy.types.Panel):
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Symmetrize Weld"
    bl_idname = "xx_sculpt_symmetrize_weld_panel"

    def draw(self, context):
        layout = self.layout
        sculpt = context.tool_settings.sculpt
        layout.prop(sculpt, "symmetrize_direction")
        # When active_default=true, an operator button defined after this will be activated when pressing return
        layout.active_default = True
        layout.operator("sculpt.symmetrize")


# Sculpt Parts


class SculptHoveredLoosePartSeparateOperator(bpy.types.Operator):
    bl_label = "Sculpt Hovered Loose Part Separate"
    bl_idname = "sculpt.xx_sculpt_hovered_loose_part_separate"
    bl_options = {'REGISTER', 'UNDO'}

    event = {}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.data

    def invoke(self, context, event):
        self.event = yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        deselectAllExceptActiveInContext(context)

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        succeed = selectFaceUnderMouseFromContextEvent(context, self.event)

        if not succeed:
            bpy.ops.sculpt.sculptmode_toggle()
            return {'FINISHED'}

        # / Seprarate Hovered Loose Parts
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_linked(delimit={'NORMAL'})
        # Show hovered loose part with hidden part
        bpy.ops.mesh.reveal(select=True)
        bpy.ops.mesh.hide(unselected=True)
        obj = context.active_object
        polygonIdx = obj.data.polygons.active
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(
            mode='OBJECT')  # polygon.select works only in object mode \
        obj.data.polygons[polygonIdx].select = True
        # Select hovered loose part and separate it
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_linked(delimit={'NORMAL'})
        if not len(getSelectedVerticesOfObject(context.active_object)):
            bpy.ops.mesh.reveal(select=True)
            bpy.ops.sculpt.sculptmode_toggle()
            return {'FINISHED'}
        if areAllFacesSelectedInObject(context.active_object):
            bpy.ops.sculpt.sculptmode_toggle()
            return {'FINISHED'}
        bpy.ops.mesh.separate(type='SELECTED')
        # Hide hidden back
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.reveal(select=False)
        bpy.ops.mesh.hide(unselected=False)
        # Reset pivot to geometry to separated
        bpy.ops.object.mode_set(mode='OBJECT')
        for i, obj in enumerate(context.selected_objects):
            if obj != context.active_object:
                context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(
                    type='ORIGIN_GEOMETRY', center='MEDIAN')
            else:
                activeIdx = i
        context.view_layer.objects.active = context.selected_objects[activeIdx]
        # Restore mode
        deselectAllExceptActiveInContext(context)
        bpy.ops.sculpt.sculptmode_toggle()

        return {'FINISHED'}


class SculptHoveredObjectJoinOperator(bpy.types.Operator):
    bl_label = "Sculpt Hovered Object Join"
    bl_idname = "sculpt.xx_sculpt_hovered_object_join"
    bl_options = {'REGISTER', 'UNDO'}

    event = {}

    def invoke(self, context, event):
        self.event = yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")
        deselectAllExceptActiveInContext(context)
        succeed = selectObjectUnderMouseFromContextEvent(
            context, self.event)

        if not succeed or not context.selected_objects or len(context.selected_objects) == 1:
            bpy.ops.sculpt.sculptmode_toggle()
            return {'FINISHED'}

        bpy.ops.object.join()
        bpy.ops.sculpt.sculptmode_toggle()

        return {'FINISHED'}


class SculptRemeshByLoosePartsOperator(bpy.types.Operator):
    bl_label = "Sculpt Remesh By Loose Parts"
    bl_idname = "sculpt.xx_sculpt_remesh_by_loose_parts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        deselectAllExceptActiveInContext(context)

        bpy.ops.mesh.separate(type='LOOSE')

        bpy.ops.object.mode_set(mode='OBJECT')
        mainObjName = context.active_object.name

        for obj in context.selected_objects:
            if obj.name != mainObjName:
                context.view_layer.objects.active = obj
                bpy.ops.sculpt.sculptmode_toggle()
                bpy.ops.object.voxel_remesh()
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                mainObj = obj

        context.view_layer.objects.active = mainObj
        bpy.ops.sculpt.sculptmode_toggle()
        bpy.ops.object.voxel_remesh()
        bpy.ops.object.join()

        return {'FINISHED'}


# / Paint Tools


class PaintGradientSettingsPanelOperator(bpy.types.Operator):
    bl_label = "Paint Gradient Settings Panel"
    bl_idname = "paint.xx_paint_gradient_panel"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            brush = context.scene.tool_settings.image_paint.brush
        except Exception as er:
            brush = None
        return brush

    def execute(self, context):
        brush = context.scene.tool_settings.image_paint.brush
        if not brush.color_type == 'GRADIENT':
            self.report({'INFO'}, "Brush color hasn't set to gradient!")
            return {'FINISHED'}

        bpy.ops.wm.call_panel(
            name=PaintGradientSettingsPanel.bl_idname)
        return {'FINISHED'}


class PaintGradientSettingsPanel(bpy.types.Panel):
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Gradient"
    bl_idname = "xx_paint_gradient_panel"

    @classmethod
    def prop_unified(
        cls,
        layout,
        context,
        brush,
        prop_name,
        unified_name=None,
        pressure_name=None,
        icon='NONE',
        text=None,
        slider=False,
        header=False,
    ):
        """ Generalized way of adding brush options to the UI,
            along with their pen pressure setting and global toggle, if they exist. """
        row = layout.row(align=True)
        ups = context.tool_settings.unified_paint_settings
        prop_owner = brush
        if unified_name and getattr(ups, unified_name):
            prop_owner = ups

        row.prop(prop_owner, prop_name, icon=icon, text=text, slider=slider)

        if pressure_name:
            row.prop(brush, pressure_name, text="")

        if unified_name and not header:
            # NOTE: We don't draw UnifiedPaintSettings in the header to reduce clutter. D5928#136281
            row.prop(ups, unified_name, text="", icon='BRUSHES_ALL')

        return row

    def draw(self, context):
        layout = self.layout
        brush = context.scene.tool_settings.image_paint.brush

        layout.template_color_ramp(brush, "gradient", expand=True)

        layout.use_property_split = True

        col = layout.column()

        if brush.image_tool == 'DRAW':
            self.prop_unified(
                col,
                context,
                brush,
                "secondary_color",
                unified_name="use_unified_color",
                text="Background Color",
                header=True,
            )

            col.prop(brush, "gradient_stroke_mode", text="Gradient Mapping")

            if brush.gradient_stroke_mode in {'SPACING_REPEAT', 'SPACING_CLAMP'}:
                col.prop(brush, "grad_spacing")


class PaintColorPalettePanelOperator(bpy.types.Operator):
    bl_label = "Paint Color Palette Panel"
    bl_idname = "paint.xx_paint_color_palette_panel"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_panel(
            name=PaintColorPalettePanel.bl_idname)
        return {'FINISHED'}


class PaintColorPalettePanel(bpy.types.Panel):
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Color Palette"
    bl_idname = "xx_paint_color_palette_panel"
    bl_ui_units_x = 10  # width

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        paint = context.scene.tool_settings.vertex_paint if (
            'VERTEX' in context.mode) else context.scene.tool_settings.image_paint
        uniPaint = context.scene.tool_settings.unified_paint_settings
        paintBrush = uniPaint if uniPaint.use_unified_color else paint.brush

        if context.object:
            sub_row = layout.row(align=True)
            sub_row.prop(paintBrush, "color", text="")

            row = layout.row(align=True)
            row.template_ID(paint, "palette", new="palette.new")

            if paint.palette:
                layout.template_palette(paint, "palette", color=True)


class PaintMaskImageInvertOperator(bpy.types.Operator):
    bl_label = "Paint Mask Image Invert"
    bl_idname = "paint.xx_paint_stencil_mask_image_invert"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            hasStencilImage = context.tool_settings.image_paint.stencil_image
        except Exception as er:
            hasStencilImage = None

        if not hasStencilImage:
            self.report({'INFO'}, "Mask stencil image hasn't been set!")
            return {'FINISHED'}

        img = context.tool_settings.image_paint.stencil_image
        bpy.ops.image.invert(
            {'edit_image': bpy.data.images[img.name]},
            invert_r=True, invert_g=True, invert_b=True)

        return {'FINISHED'}


# / Image/Shading Tools (Resources)


# Pack


class PackAllSavedOperator(bpy.types.Operator):
    """Pack all saved instances into the .blend file."""
    bl_label = "Pack All Saved"
    bl_idname = "file.xx_pack_all_saved"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            bpy.ops.file.pack_all()
            self.report({'INFO'}, "All saved resources are packed!")
        except Exception as er:
            self.report({'ERROR'}, "{0}".format(er))

        return {'FINISHED'}


class ImagePackOperator(bpy.types.Operator):
    bl_label = "Image Pack"
    bl_idname = "file.xx_image_pack"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.image.pack()
        return {'FINISHED'}


class ImageUnpackOperator(bpy.types.Operator):
    bl_label = "Image Unpack"
    bl_idname = "file.xx_image_unpack"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.image.unpack(method='WRITE_ORIGINAL')
        return {'FINISHED'}


# Create New


class ShadingCreateNewOperator(bpy.types.Operator):
    bl_label = "Shading New"
    bl_idname = "node.xx_shader_new"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            isShading = context.space_data.tree_type == 'ShaderNodeTree'
        except Exception as er:
            isShading = None
        return isShading

    def execute(self, context):
        snode = context.space_data
        if snode.shader_type == 'OBJECT':
            mat = bpy.data.materials.new('Material')
            mat.use_nodes = True
            context.active_object.active_material = mat
        elif snode.shader_type == 'WORLD':
            world = bpy.data.worlds.new("World")
            world.use_nodes = True
            context.scene.world = world
        elif snode.shader_type == 'LINESTYLE':
            bpy.ops.scene.freestyle_linestyle_new()
        return {'FINISHED'}


# Set Active


class ImageSetActiveMenuOperator(bpy.types.Operator):
    bl_label = "Image Set Active Menu"
    bl_idname = "image.xx_image_set_active_menu"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        bpy.ops.wm.call_menu(name=ImageSetActiveMenu.bl_idname)
        return {'FINISHED'}


class ImageSetActiveMenu(bpy.types.Menu):
    bl_label = "Set Active"
    bl_idname = "xx_image_set_active_menu"

    def draw(self, context):
        global glob
        editor_space = getSpaceUnderMouseFromContextEvent(context, glob.event)
        layout = self.layout
        with context.temp_override(space=editor_space):
            layout.template_ID(editor_space, "image")


class ShadingSetActiveMenuOperator(bpy.types.Operator):
    bl_label = "Shading Set Active Menu"
    bl_idname = "node.xx_shader_set_active_menu"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            isShading = context.space_data.tree_type == 'ShaderNodeTree'
        except Exception as er:
            isShading = None
        return isShading

    def invoke(self, context, event):
        yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        bpy.ops.wm.call_menu(name=ShadingSetActiveMenu.bl_idname)
        return {'FINISHED'}


class ShadingSetActiveMenu(bpy.types.Menu):
    bl_label = "Set Active"
    bl_idname = "xx_shader_set_active_menu"

    def draw(self, context):
        global glob
        layout = self.layout
        editor_space = getSpaceUnderMouseFromContextEvent(context, glob.event)
        snode = context.space_data

        if snode.shader_type == 'OBJECT' and context.object:
            with context.temp_override(space=editor_space):
                layout.template_ID(
                    context.object, "active_material", new="material.new")
        elif snode.shader_type == 'WORLD':
            scene = context.scene
            with context.temp_override(space=editor_space):
                layout.template_ID(
                    scene, "world", new="world.new")
        elif snode.shader_type == 'LINESTYLE':
            lineset = context.view_layer.freestyle_settings.linesets.active
            with context.temp_override(space=editor_space):
                layout.template_ID(
                    lineset, "linestyle", new="scene.freestyle_linestyle_new")


# Keep Fake User


class ImageKeepFakeUserOperator(bpy.types.Operator):
    bl_label = "Image Keep Fake User"
    bl_idname = "image.xx_image_keep_fake_user"
    bl_options = {'REGISTER', 'UNDO'}

    event = {}

    def invoke(self, context, event):
        self.event = yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        space = getSpaceUnderMouseFromContextEvent(context, self.event)
        if space.image:
            space.image.use_fake_user = True if not space.image.use_fake_user else False
            # Refresh/update ui header
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}


class ShadingKeepFakeUserOperator(bpy.types.Operator):
    bl_label = "Shading Keep Fake User"
    bl_idname = "node.xx_shader_keep_fake_user"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            isShading = context.space_data.tree_type == 'ShaderNodeTree'
        except Exception as er:
            isShading = None
        return isShading

    def execute(self, context):
        snode = context.space_data

        if snode.shader_type == 'OBJECT':
            mat = context.active_object.active_material
            if mat:
                mat.use_fake_user = True if not mat.use_fake_user else False
        elif snode.shader_type == 'WORLD':
            world = context.scene.world
            if world:
                world.use_fake_user = True if not world.use_fake_user else False
        elif snode.shader_type == 'LINESTYLE':
            lineset = context.view_layer.freestyle_settings.linesets.active
            if lineset:
                linestyle = lineset.linestyle
                linestyle.use_fake_user = True if not linestyle.use_fake_user else False

        # Refresh/update ui header
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}


# Make Single Copy


class ImageMakeSingleCopyOperator(bpy.types.Operator):
    bl_label = "Image Make Single Copy"
    bl_idname = "image.xx_image_make_single_copy"
    bl_options = {'REGISTER', 'UNDO'}

    event = {}

    def invoke(self, context, event):
        self.event = yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        space = getSpaceUnderMouseFromContextEvent(context, self.event)
        space.image = space.image.copy()
        return {'FINISHED'}


class MaterialMakeSingleCopyOperator(bpy.types.Operator):
    bl_label = "Material Make Single Copy"
    bl_idname = "node.xx_material_make_single_copy"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            isShading = context.space_data.tree_type == 'ShaderNodeTree'
        except Exception as er:
            isShading = None
        return isShading

    def execute(self, context):
        snode = context.space_data
        if snode.shader_type == 'OBJECT':
            for obj in context.selected_objects:
                mat = obj.active_material
                if mat:
                    obj.active_material = mat.copy()
        return {'FINISHED'}


# Close


class ImageCloseOperator(bpy.types.Operator):
    bl_label = "Image Close"
    bl_idname = "image.xx_image_close"
    bl_options = {'REGISTER', 'UNDO'}

    event = {}

    def invoke(self, context, event):
        self.event = yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        space = getSpaceUnderMouseFromContextEvent(context, self.event)
        space.image = None
        return {'FINISHED'}


class ShadingCloseOperator(bpy.types.Operator):
    bl_label = "Shading Close"
    bl_idname = "node.xx_shader_close"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            isShading = context.space_data.tree_type == 'ShaderNodeTree'
        except Exception as er:
            isShading = None
        return isShading

    def execute(self, context):
        snode = context.space_data
        if snode.shader_type == 'OBJECT':
            context.active_object.active_material = None
        elif snode.shader_type == 'WORLD':
            context.scene.world = None
        return {'FINISHED'}


# Remove


class ImageRemoveOperator(bpy.types.Operator):
    bl_label = "Image Remove"
    bl_idname = "image.xx_image_remove"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        space = getSpaceUnderMouseFromContextEvent(context, event)
        if bool(space) and bool(space.image):
            return self.execute(context)
        else:
            return {'CANCELLED'}

    def execute(self, context):
        bpy.ops.wm.call_menu(name=ImageRemoveConfirmMenu.bl_idname)
        return {'FINISHED'}


class ImageRemoveConfirmMenu(bpy.types.Menu):
    bl_label = "OK?"
    bl_idname = "xx_image_remove_confirm_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator(
            ImageRemoveConfirmMenuOperator.bl_idname, text="Remove")


class ImageRemoveConfirmMenuOperator(bpy.types.Operator):
    bl_label = "Image Remove Confirm Menu"
    bl_idname = "image.xx_image_remove_confirm_menu"
    bl_options = {'REGISTER', 'UNDO'}

    event = {}

    def invoke(self, context, event):
        self.event = yield_global_event(event)
        return self.execute(context)

    def execute(self, context):
        space = getSpaceUnderMouseFromContextEvent(context, self.event)
        if not space.image.use_fake_user:
            img = space.image
            img.user_clear()
            bpy.data.images.remove(img, do_unlink=True,
                                   do_id_user=True, do_ui_user=True)
        else:
            self.report(
                {'INFO'}, "Can't remove image while fake user is turned on!")
        return {'FINISHED'}


class ShadingRemoveOperator(bpy.types.Operator):
    bl_label = "Shading Remove"
    bl_idname = "node.xx_shader_remove"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.wm.call_menu(name=ShadingRemoveConfirmMenu.bl_idname)
        return {'FINISHED'}


class ShadingRemoveConfirmMenu(bpy.types.Menu):
    bl_label = "OK?"
    bl_idname = "xx_shader_remove_confirm_menu"

    @classmethod
    def poll(cls, context):
        snode = context.space_data
        if snode.shader_type == 'OBJECT':
            act = context.active_object.active_material
        elif snode.shader_type == 'WORLD':
            act = context.scene.world

        try:
            isShading = context.space_data.tree_type == 'ShaderNodeTree'
        except Exception as er:
            isShading = None
        return isShading and act

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator(
            ShadingRemoveConfirmMenuOperator.bl_idname, text="Remove")


class ShadingRemoveConfirmMenuOperator(bpy.types.Operator):
    bl_label = "Shading Remove"
    bl_idname = "node.xx_shader_remove_confirm_menu"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        snode = context.space_data
        if snode.shader_type == 'OBJECT':
            mat = context.active_object.active_material
            if not mat.use_fake_user:
                mat.user_clear()
                bpy.data.materials.remove(
                    mat, do_unlink=True, do_id_user=True, do_ui_user=True)
            else:
                self.report(
                    {'INFO'}, "Can't remove instance while fake user is turned on!")
        elif snode.shader_type == 'WORLD':
            world = context.scene.world
            if not world.use_fake_user:
                world.user_clear()
                bpy.data.worlds.remove(
                    world, do_unlink=True, do_id_user=True, do_ui_user=True)
            else:
                self.report(
                    {'INFO'}, "Can't remove image while fake user is turned on!")

        return {'FINISHED'}
