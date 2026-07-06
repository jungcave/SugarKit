import bpy
import math
import functools
from .SugarUtils import C, CD, CL
from .SugarUtils import (
    restoreDefaultKeymaps,
    buildNewActiveKeyconfig,
    disableIncludingHotkeysInKeyconfig,
    clearAllInactiveKeymapItemsInKeyconfig,
    saveAndExportKeyconfig,
)
from .SugarUtils import addKeymapItem as add
from .SugarUtils import disableKeymapItem as disable
from .SugarUtils import editUserKeymapItem as edit


INDEXES = ['ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE',
           'SIX', 'SEVEN', 'EIGHT', 'NINE']
NUMBERS = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE',
           'SIX', 'SEVEN', 'EIGHT', 'NINE', 'ZERO']


class BuildSugarKeyconfigOperator(bpy.types.Operator):
    bl_label = 'Build Sugar Hotkeys'
    bl_idname = 'window.xx_build_sugar_keyconfig'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        restoreDefaultKeymaps()

        nkc = buildNewActiveKeyconfig('Sugar Hotkeys')

        disableIncludingHotkeysInKeyconfig(
            nkc, ['cmd', 'Numpad', 'NDOF'], excludes=[
                'cmd A', 'cmd S', 'cmd D', 'cmd Z', 'shift cmd Z', 'cmd X', 'cmd C', 'cmd V', 'cmd LEFTMOUSE'])

        # INTERFACE
        self.addInterfaceHotkeys()
        # VIEW
        self.addViewHotkeys()
        # OBJECT
        self.addObjectHotkeys()
        # OUTLINER
        self.addOutlinerHotkeys()
        # TRANSFORMATIONS
        self.addTransformationsHotkeys()
        # PROPERTIES
        self.addPropertiesHotkeys()
        # ANIMATION
        self.addAnimationHotkeys()
        # EDIT MESH
        self.addEditMeshHotkeys()
        # CURVES
        self.addCurvesHotkeys()
        # ARMATURE
        self.addArmatureHotkeys()
        # FONT
        self.addFontHotkeys()
        # SCULPT
        self.addSculptHotkeys()
        # PAINT
        self.addPaintHotkeys()
        # IMAGE/UV
        self.addImageAndUvHotkeys()
        # FILE BROWSER
        self.addFileBrowserHotkeys()
        # SHADER
        self.addShaderHotkeys()

        # ADDONS {b}
        bpy.app.timers.register(
            functools.partial(self.editOtherAddonsHotkeys), first_interval=0.1)  # must run async to prevent user kyconf collision with clearAllInactiveKeymapItemsInKeyconfig \

        clearAllInactiveKeymapItemsInKeyconfig(nkc)

        bpy.app.timers.register(
            functools.partial(saveAndExportKeyconfig, 'Sugar_Hotkeys.py'), first_interval=0.2)  # must run async to properly cache changes after editOtherAddonsHotkeys and clearAllInactiveKeymapItemsInKeyconfig \

        return {'FINISHED'}

    @classmethod
    def addInterfaceHotkeys(cls):
        disable('Window', 'wm.quit_blender', 'Q ctrl')

        # file
        add('Window', 'wm.save_as_mainfile',
            'S ctrl alt', disableOld='S shift ctrl')

        add('Window', {'wm.call_menu': {'name': 'TOPBAR_MT_file_new'}},
            'SPACE TAB', head=True)
        add('Window', 'wm.open_mainfile',
            'LEFT_CTRL TAB')
        add('Window', {'wm.call_menu': {'name': 'TOPBAR_MT_file_open_recent'}},
            'LEFT_SHIFT TAB')

        add('Window', 'wm.obj_import',
            'I shift ctrl')
        add('Window', 'wm.obj_import',
            'W shift ctrl')
        add('Window', 'import_scene.fbx',
            'I shift ctrl alt')
        add('Window', 'import_scene.fbx',
            'W shift ctrl alt')
        add('Window', 'wm.obj_export',
            'E shift ctrl')
        add('Window', 'export_scene.fbx',
            'E shift ctrl alt')
        add('Window', 'wm.append',
            'A shift ctrl alt')

        # edit preferences
        add('Screen', 'screen.userpref_show',
            'SPACE shift ctrl alt')

        # cycle workspace
        for k, v in {'RIGHT_ARROW': 'NEXT', 'LEFT_ARROW': 'PREV'}.items():
            add('Screen', 'screen.workspace_cycle',
                k + ' shift ctrl', setKmiProps=lambda kmi: setDirectionProp(kmi, v))

        # viewport area
        add('Screen', 'screen.area_close',
            'X shift ctrl alt')
        for kmn in [
            'Window',
            'Object Mode',
            'Outliner',
            'Mesh',
            'Sculpt',
            'Vertex Paint',
            'Weight Paint',
            'Image Paint',
            'Image',
            'UV Editor',
            'File Browser',
            'Node Editor',
        ]:
            for k, v in {
                'ONE': 'VIEW_3D',
                'TWO': 'IMAGE_EDITOR',
                'THREE': 'NODE_EDITOR',
                'FOUR': 'SEQUENCE_EDITOR',  # Video
                'FOUR DOUBLE_CLICK': 'CLIP_EDITOR',  # Movie
                'FIVE': 'DOPESHEET_EDITOR',  # Timeline
                'SIX': 'GRAPH_EDITOR',
                'SEVEN': 'TEXT_EDITOR',
                'EIGHT': 'INFO',
                'ACCENT_GRAVE': 'CONSOLE',
                'NINE': 'OUTLINER',
                'Z': 'OUTLINER',
                'ZERO': 'PROPERTIES',
                'X': 'PROPERTIES',
                'SPACE': 'FILE_BROWSER'
            }.items():
                add(kmn, 'screen.space_type_set_or_cycle',
                    k + ' Q', setKmiProps=lambda kmi: setSpaceTypeProp(kmi, v), head=True)

    @classmethod
    def addViewHotkeys(cls):
        # navigation
        add('3D View', {'view3d.view_axis': {'relative': True}},
            'TRACKPADPAN alt ANY', setKmiProps=lambda kmi: setTypeProp(kmi, 'FRONT'))
        disable('3D View', 'view3d.view_all',
                'C shift')
        for kmn in ['View2D', '3D View', 'Image']:
            disable(kmn, '*.zoom_border',
                    'B shift')
        disable('3D View', 'view3d.zoom',
                'MINUS shift ctrl')
        disable('3D View', 'view3d.zoom',
                'EQUAL shift ctrl')
        add('Image', 'image.view_pan',
            'TRACKPADPAN shift ANY')
        add('Node Editor', 'view2d.pan',
            'TRACKPADPAN shift ANY')

        for kmn in ['Object Mode', 'Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']:
            for k, v in {'ONE': 'RIGHT', 'TWO': 'FRONT', 'THREE': 'TOP'}.items():
                add(kmn, 'view3d.view_axis',
                    k + ' SPACE', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)
                add(kmn, {'view3d.view_axis': {'align_active': True}},
                    k + ' ACCENT_GRAVE repeat', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)

            for k, v in {'ONE': 'LEFT', 'TWO': 'BACK', 'THREE': 'BOTTOM'}.items():
                add(kmn, 'view3d.view_axis',
                    k + ' SPACE DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)

            for k, v in {'FOUR': 'ORBITLEFT', 'FIVE': 'ORBITDOWN'}.items():
                add(kmn, {'view3d.view_orbit': {'angle': math.radians(180)}},
                    k + ' SPACE', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)

            for k, v in {
                'W': 'ORBITUP',
                'A': 'ORBITLEFT',
                'S': 'ORBITDOWN',
                'D': 'ORBITRIGHT',
            }.items():
                add(kmn, 'view3d.view_orbit',
                    k + ' SPACE', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)
                add(kmn, 'view3d.view_orbit',
                    k + ' SPACE DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)

            for k, v in {'Q': 'LEFT', 'E': 'RIGHT'}.items():
                add(kmn, {'view3d.view_roll': {'angle': -0.392699 if v == 'LEFT' else 0.392699}},  # 22.5 deg
                    k + ' SPACE', setKmiProps=lambda kmi: setTypeProp(kmi, v), head=True)
                add(kmn, {'view3d.view_roll': {'angle': -1.178097 if v == 'LEFT' else 1.178097}},  # 67.5 deg
                    k + ' SPACE DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'ANGLE'), head=True)

        # annotate
        for kmn in ['Grease Pencil', '3D View Tool: Tweak']:
            add(kmn, {'gpencil.annotate': {'wait_for_input': False}},
                'LEFTMOUSE X', disableOld='LEFTMOUSE D', setKmiProps=lambda kmi: setModeProp(kmi, 'DRAW'), head=True)
        for k in ['LEFTMOUSE shift D', 'LEFTMOUSE alt D', 'LEFTMOUSE shift alt D']:
            disable('Grease Pencil', 'gpencil.annotate', k)
        add('Grease Pencil', {'gpencil.annotate': {'wait_for_input': True}},
            'RIGHTMOUSE X', setKmiProps=lambda kmi: setModeProp(kmi, 'DRAW_POLY'))
        for kmn in ['Grease Pencil', '3D View Tool: Tweak']:
            add(kmn, {'gpencil.annotate': {'wait_for_input': False}},
                'LEFTMOUSE Z', disableOld='RIGHTMOUSE D', setKmiProps=lambda kmi: setModeProp(kmi, 'ERASER'), head=True)
        for kmn in ['Annotate', 'Annotate Line', 'Annotate Polygon']:
            add('Generic Tool: ' + kmn, {'gpencil.annotate': {'wait_for_input': False}},
                'LEFTMOUSE Z', setKmiProps=lambda kmi: setModeProp(kmi, 'ERASER'), head=True)
        add('Grease Pencil', 'gpencil.layer_annotation_remove',
            'RIGHTMOUSE Z')

        # tools
        for kmn in [
            'Object Mode',
            'Mesh',
            'Sculpt',
            'Vertex Paint',
            'Weight Paint',
            'Image Paint',
            'Image',
            'UV Editor',
            'Node Editor'
        ]:
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin.annotate'}},
                'A X', head=True)
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin.annotate_eraser'}},
                'A X DOUBLE_CLICK', head=True)
        for kmn in [
            'Object Mode',
            'Mesh',
            'Sculpt',
            'Vertex Paint',
            'Weight Paint',
            'Image Paint'
        ]:
            add(kmn, {'wm.call_panel': {'name': 'TOPBAR_PT_annotation_layers'}},
                'A Z', head=True)
        for kmn in ['Object Mode', 'Mesh']:
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin.measure'}},
                'W X', head=True)
        add('3D View Tool: Measure', 'view3d.ruler_remove',
            'X ctrl', disableOld='X')
        add('3D View Tool: Measure', 'view3d.ruler_remove',
            'BACK_SPACE CLICK', disableOld='DEL')

        # view
        add('3D View', 'view3d.navigate',
            'LEFT_SHIFT SPACE', disableOld='ACCENT_GRAVE shift')

        for kmn, v in {
            'Outliner': 'OUTLINER',
            'Dopesheet': 'DOPESHEET',
            '3D View': 'VIEW3D',
            'Graph Editor': 'GRAPH',
            'Image Generic': 'IMAGE',
            'Node Editor': 'NODE',
            'File Browser': 'FILEBROWSER',  # display mode
            'NLA Editor': 'NLA',
            'Sequencer': 'SEQUENCER',
            'SequencerPreview': 'SEQUENCER_',
            'Clip': 'CLIP'
        }.items():
            add(kmn, {'wm.call_menu_pie': {'name': v + '_MT_view_pie'}},
                'ACCENT_GRAVE ctrl', disableOld='ACCENT_GRAVE')

        add('3D View', 'view3d.view_persportho',
            'ACCENT_GRAVE alt')
        add('3D View', 'view3d.view_persportho',
            'SPACE ACCENT_GRAVE', head=True)

        add('Screen', 'screen.region_quadview',
            'Q shift ctrl alt', disableOld='Q ctrl alt')

        # view camera
        add('3D View', 'view3d.view_camera',
            'ZERO')
        for kmn in ['Object Mode', 'Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']:
            add(kmn, 'view3d.view_camera',
                'TAB SPACE', head=True)
        add('3D View', 'view3d.object_as_camera',
            'ZERO ctrl')
        add('3D View', 'view3d.object_as_camera',
            'LEFT_CTRL SPACE')
        add('3D View', 'view3d.camera_to_view',
            'ZERO alt')
        add('3D View', 'view3d.camera_to_view',
            'LEFT_ALT SPACE')

        # view region
        add('3D View', 'view3d.render_border',
            'X Z', disableOld='B ctrl')
        add('3D View', 'view3d.clear_render_border',
            'Z X', disableOld='B ctrl alt')
        add('Image', 'image.render_border',
            'X Z', disableOld='B ctrl')
        add('Image', 'image.clear_render_border',
            'Z X', disableOld='B ctrl alt')
        add('Node Editor', 'node.viewer_border',
            'X Z', disableOld='B ctrl')
        add('Node Editor', 'node.clear_viewer_border',
            'Z X', disableOld='B ctrl alt')
        add('3D View', 'view3d.clip_border',
            'C Z', disableOld='B alt')

        # view interface
        add('Screen', 'screen.screen_full_area',
            'BACK_SLASH', disableOld='SPACE ctrl')
        add('Screen', 'screen.screen_full_area',
            'Q ACCENT_GRAVE', head=True)
        add('Screen', {'screen.screen_full_area': {'use_hide_panels': True}},
            'BACK_SLASH alt', disableOld='SPACE ctrl alt')
        add('Screen', {'screen.screen_full_area': {'use_hide_panels': True}},
            'TAB ACCENT_GRAVE', head=True)
        for kmn in [
            'Dopesheet Generic',
            '3D View Generic',
            'Graph Editor Generic',
            'Image Generic',
            'Node Generic',
            'NLA Generic',
            'SequencerCommon',
            'Clip',
            'Spreadsheet Generic'
        ]:
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.show_region_ui'}},
                'SLASH', disableOld='N')
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.show_region_ui'}},
                'LEFT_SHIFT ACCENT_GRAVE')
        add('File Browser', 'screen.region_toggle',
            'SLASH', setKmiProps=lambda kmi: setRegionTypeProp(kmi, 'TOOL_PROPS'))
        add('File Browser', 'screen.region_toggle',
            'LEFT_SHIFT ACCENT_GRAVE repeat', setKmiProps=lambda kmi: setRegionTypeProp(kmi, 'TOOL_PROPS'))

        for kmn in [
            '3D View Generic',
            'Image Generic',
            'Node Generic',
            'File Browser',
            'SequencerCommon',
            'Clip',
            'Spreadsheet Generic'
        ]:
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.show_region_toolbar'}},
                'SLASH alt', disableOld='T')
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.show_region_toolbar'}},
                'LEFT_ALT ACCENT_GRAVE', disableOld='T')
        add('Window', {'wm.context_toggle': {'data_path': 'space_data.show_region_tool_header'}},
            'SLASH ctrl')
        add('Window', {'wm.context_toggle': {'data_path': 'space_data.show_region_tool_header'}},
            'LEFT_CTRL ACCENT_GRAVE')
        add('File Browser', {'wm.context_toggle': {'data_path': 'space_data.show_region_ui'}},
            'SLASH ctrl', disableOld='N')
        add('File Browser', {'wm.context_toggle': {'data_path': 'space_data.show_region_ui'}},
            'LEFT_CTRL ACCENT_GRAVE')

        # gizmo
        for kmn in ['3D View', 'UV Editor', 'Image', 'SequencerPreview']:
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.show_gizmo'}},
                'COMMA alt', disableOld='ACCENT_GRAVE ctrl')
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.show_gizmo'}},
                'X ACCENT_GRAVE', head=True)

        # overlays
        for kmn, v in {
            '3D View': 'VIEW3D_PT_overlay',
            'Image': 'IMAGE_PT_overlay',
            'Node Editor': 'NODE_PT_overlay'
        }.items():
            add(kmn, {'wm.call_panel': {'name': v}},
                'SPACE ctrl alt')
        for kmn in [
            '3D View',
            'UV Editor',
            'Image',
            'Node Editor',
            'Sequencer',
            'SequencerPreview'
        ]:
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.overlay.show_overlays'}},
                'PERIOD alt', disableOld='Z shift alt')
            add(kmn, {'wm.context_toggle': {'data_path': 'space_data.overlay.show_overlays'}},
                'Z ACCENT_GRAVE', head=True)

        for k, v in {
            'PERIOD': 'show_floor',
            'COMMA': 'show_ortho_grid',
            'W': 'show_wireframes',
            'N': 'show_face_orientation',
        }.items():
            add('3D View', {'wm.context_toggle': {'data_path': 'space_data.overlay.' + v}},
                k + ' ctrl alt')
        add('3D View', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_floor'}},
            'ACCENT_GRAVE ctrl alt')
        add('3D View', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_ortho_grid'}},
            'ACCENT_GRAVE ctrl alt RELEASE')
        add('3D View', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_face_orientation'}},
            'SPACE Z', head=True)

        # x-ray
        add('3D View', 'view3d.toggle_xray',
            'COMMA', disableOld='Z alt')
        add('3D View', 'view3d.toggle_xray',
            'LEFT_SHIFT Z')

        # shading
        add('3D View', {'wm.call_panel': {'name': 'VIEW3D_PT_shading'}},
            'TAB ctrl alt')
        add('3D View', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_shading_pie'}},
            'PERIOD shift', disableOld='Z')
        add('3D View', {'wm.context_menu_enum': {'data_path': 'space_data.shading.type'}},
            'Z shift')

        add('3D View', 'view3d.toggle_shading',
            'PERIOD', disableOld='Z shift')
        add('3D View', 'view3d.toggle_shading',
            'LEFT_ALT Z')
        add('3D View', {'wm.context_menu_enum': {'data_path': 'space_data.shading.wireframe_color_type'}},
            'PERIOD shift alt')

        add('3D View', 'view3d.toggle_shading',
            'PERIOD DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'SOLID'))
        add('3D View', {'wm.context_set_enum': {'data_path': 'space_data.shading.type'}},
            'Z alt DOUBLE_CLICK', setKmiProps=lambda kmi: setValueProp(kmi, 'SOLID'))
        for kmn in ['Object Mode', 'Mesh', 'Sculpt']:
            add(kmn, {'wm.context_menu_enum': {'data_path': 'space_data.shading.color_type'}},
                'COMMA shift alt')
            add(kmn, {'wm.context_menu_enum': {'data_path': 'space_data.shading.color_type'}},
                'Z shift alt')
        add('3D View', 'view3d.toggle_shading',
            'Z alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'MATERIAL'))
        add('3D View', 'view3d.toggle_shading',
            'TAB Z', setKmiProps=lambda kmi: setTypeProp(kmi, 'RENDERED'), head=True)

        for k, v in {
            'C': 'show_cavity',
            'E CLICK': 'use_scene_world'
        }.items():
            add('3D View', {'wm.context_toggle': {'data_path': 'space_data.shading.' + v}},
                k + ' ctrl alt')
        add('Window', {'wm.context_toggle': {'data_path': 'space_data.shading.use_scene_world_render'}},
            'E ctrl alt RELEASE')
        add('3D View', {'wm.context_toggle': {'data_path': 'scene.render.film_transparent'}},
            'LEFTMOUSE ctrl alt E')

        # render
        add('Window', {'wm.context_menu_enum': {'data_path': 'scene.render.engine'}},
            'TAB shift ctrl alt')
        add('Screen', {'render.render': {'use_viewport': True}},
            'R shift ctrl alt')
        add('Screen', {'render.render': {'use_viewport': True, 'animation': True}},
            'QUOTE shift ctrl alt')
        add('Screen', 'render.opengl',
            'V shift ctrl alt repeat')
        add('Screen', {'render.opengl': {'animation': True}},
            'SEMI_COLON shift ctrl alt repeat')

        # object data props
        for kmn in ['Object Mode', 'Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']:
            add(kmn, {'wm.context_toggle': {'data_path': 'object.show_in_front'}},
                'ONE Z', head=True)
            add(kmn, {'wm.context_toggle': {'data_path': 'object.show_wire'}},
                'TWO Z', head=True)
        add('3D View', {'wm.context_menu_enum': {'data_path': 'object.display_type'}},
            'COMMA ctrl')
        add('3D View', {'wm.context_menu_enum': {'data_path': 'object.display_type'}},
            'LEFT_CTRL Z')

    @classmethod
    def addObjectHotkeys(cls):
        # mode
        add('Object Non-modal', {'object.mode_set': {'toggle': False}},
            'LEFT_ALT TAB', setKmiProps=lambda kmi: setModeProp(kmi, 'OBJECT'))
        for kmn in ['Object Non-modal', 'Image']:
            add(kmn, {'object.mode_set': {'toggle': True}},
                'TAB CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'EDIT'), disableOld='TAB')
        for kmn in ['Object Non-modal', 'Object Mode', 'Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']:
            add(kmn, 'object.mode_set',
                'TAB alt', setKmiProps=lambda kmi: setModeProp(kmi, 'SCULPT'))
            add(kmn, 'object.mode_set',
                'ONE TAB', setKmiProps=lambda kmi: setModeProp(kmi, 'VERTEX_PAINT'), head=True)
            add(kmn, 'object.mode_set',
                'TWO TAB', setKmiProps=lambda kmi: setModeProp(kmi, 'WEIGHT_PAINT'), head=True)
            add(kmn, 'object.mode_set',
                'THREE TAB', setKmiProps=lambda kmi: setModeProp(kmi, 'TEXTURE_PAINT'), head=True)

        add('Object Non-modal', 'object.transfer_mode',
            'RIGHTMOUSE alt CLICK', disableOld='Q alt')

        # tools
        add('Window', 'wm.toolbar_fallback_pie',
            'LEFTMOUSE W', disableOld='W alt')
        add('Window', {'wm.tool_set_by_id': {'name': 'builtin.select'}},
            'W CLICK')
        for kmn in ['3D View', 'UV Editor', 'Node Editor']:
            disable(kmn, {'wm.tool_set_by_id': {'name': 'builtin.select_box', 'cycle': True}},
                    'W')

        # 3d-cursor
        for kmn, v in {
            'Dopesheet': 'DOPESHEET',
            'Grease Pencil Stroke Edit Mode': 'GPENCIL',
            '3D View': 'VIEW3D',
            'UV Editor': 'IMAGE',
            'Graph Editor': 'GRAPH',
            'NLA Editor': 'NLA'
        }.items():
            add(kmn, {'wm.call_menu_pie': {'name': v + '_MT_snap_pie'}},
                'LEFTMOUSE Q', disableOld='S shift', head=True)
        add('3D View', 'view3d.cursor3d',
            'RIGHTMOUSE shift CLICK', disableOld='RIGHTMOUSE shift')
        add('3D View', 'view3d.snap_cursor_to_center',
            'Q DOUBLE_CLICK')
        add('3D View', 'view3d.snap_cursor_to_selected',
            'Q CLICK')

        # view
        disable('Image', 'image.view_zoom_border', 'B shift')
        for kmn, v in {
            '3D View': 'view3d.',
            'Object Mode': 'view3d.',
            'Mesh': 'view3d.',
            'Sculpt': 'view3d.',
            'Vertex Paint': 'view3d.',
            'Weight Paint': 'view3d.',
            'Image Paint': 'view3d.',
            'Dopesheet': 'action.',
            'Animation Channels': 'anim.channels_',
            'Graph Editor': 'graph.',
            'Image': 'image.',
            'Node Editor': 'node.',
            'File Browser Main': 'file.',
            'NLA Editor': 'nla.',
            'Sequencer': 'sequencer.',
            'SequencerPreview': 'sequencer.',
            'Clip Editor': 'clip.'
        }.items():
            val = {'view3d.view_selected': {'use_all_regions': False}
                   } if kmn == '3D View' else v + 'view_selected'
            add(kmn, val, 'SPACE CLICK')

        for kmn, v in {
            'Object Mode': {'view3d.view_all': {'center': False}},
            'Mesh': {'view3d.view_all': {'center': False}},
            'Sculpt': {'view3d.view_all': {'center': False}},
            'Vertex Paint': {'view3d.view_all': {'center': False}},
            'Weight Paint': {'view3d.view_all': {'center': False}},
            'Image Paint': {'view3d.view_all': {'center': False}},

            'Dopesheet': 'action.view_all',
            'Graph Editor': 'graph.view_all',
            'Image': {'image.view_all': {'fit_view': True}},
            'Node Editor': 'node.view_all',
            'NLA Editor': 'nla.view_all',
            'Sequencer': 'sequencer.view_all',
            'SequencerPreview': 'sequencer.view_all_preview',
            'Clip Editor': 'clip.view_all',
            'Clip Graph Editor': 'clip.graph_view_all',
            'Clip Dopesheet Editor': 'clip.dopesheet_view_all',
        }.items():
            add(kmn, v, 'SPACE DOUBLE_CLICK')

        add('3D View', 'view3d.localview',
            'ACCENT_GRAVE CLICK', disableOld='SLASH')
        add('3D View', {'view3d.select': {'extend': True}},
            'RIGHTMOUSE ACCENT_GRAVE', head=True)
        add('3D View', 'view3d.localview_remove_from',
            'RIGHTMOUSE ACCENT_GRAVE RELEASE', disableOld='SLASH alt', head=True)

        # hide
        add('Outliner', {'object.hide_view_set': {'unselected': True}},
            'H shift')

        for kmn, v in {
            'Grease Pencil Stroke Edit Mode': 'gpencil.reveal',
            'Grease Pencil Stroke Paint Mode': 'gpencil.reveal',
            'Paint Face Mask (Weight, Vertex, Texture)': 'paint.face_vert_reveal',
            'Paint Vertex Selection (Weight, Vertex)': 'paint.face_vert_reveal',
            'Weight Paint': 'paint.face_vert_reveal',
            'Vertex Paint': 'paint.face_vert_reveal',
            'Image Paint': 'paint.face_vert_reveal',
            'Pose': 'pose.reveal',
            'Curve': {'curve.reveal': {'select': True}},
            'Sculpt': 'sculpt.reveal_all',
            'Mesh': {'mesh.reveal': {'select': True}},
            'Armature': 'armature.reveal',
            'Metaball': 'mball.reveal_metaelems',
            'Particle': 'particle.reveal',
            'UV Editor': 'uv.reveal',
            'Graph Editor Generic': 'graph.reveal',
            'Object Mode': {'object.hide_view_clear': {'select': True}},
            'Outliner': {'object.hide_view_clear': {'select': True}},
            'Outliner': 'outliner.collection_show'
        }.items():
            add(kmn, v,
                'H DOUBLE_CLICK', disableOld='H alt')

        for kmn, v in {
            'Curve': {'curve.reveal': {'select': False}},
            'Mesh': {'mesh.reveal': {'select': False}},
            'Weight Paint': 'paint.face_vert_reveal',
            'Vertex Paint': 'paint.face_vert_reveal',
            'Image Paint': 'paint.face_vert_reveal',
            'Object Mode': {'object.hide_view_clear': {'select': False}},
            'UV Editor': {'uv.reveal': {'select': False}}
        }.items():
            add(kmn, v, 'H alt')

        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, {'wm.context_toggle': {'data_path': 'object.hide_select'}},
                'L')
            add(kmn, {'wm.context_toggle': {'data_path': 'object.hide_select'}},
                'LEFT_ALT DOUBLE_CLICK')

        for kmn in ['Pose', 'Object Mode']:
            for i, n in enumerate(NUMBERS):
                add(kmn, {'object.hide_collection': {'collection_index': i + 1, 'extend': True}},
                    n + ' alt', disableOld=n + ' shift')
                add(kmn, {'object.hide_collection': {'collection_index': i + 11, 'extend': True}},
                    n + ' ctrl alt', disableOld=n + ' shift alt')
                add(kmn, {'object.hide_collection': {'collection_index': i + 1, 'extend': False}},
                    n + ' shift', disableOld=n)
                add(kmn, {'object.hide_collection': {'collection_index': i + 11, 'extend': False}},
                    n + ' shift ctrl', disableOldExactProps=n + ' alt')
        add('Object Mode', 'object.hide_collection',
            'H shift ctrl', disableOld='H ctrl')

        # tweak select
        disable('*', '*.select_box', 'B')
        disable('*', '*.select_circle', 'C')
        disable('*', '*.select_lasso', 'RIGHTMOUSE ctrl CLICK_DRAG')
        disable('*', '*.select_lasso', 'RIGHTMOUSE shift ctrl CLICK_DRAG')
        for kmn, v in {
            '3D View Tool: Tweak': 'view3d.',
            'Image Editor Tool: Uv, Tweak': 'uv.'
        }.items():
            add(kmn, v + 'select_box',
                'LEFTMOUSE CLICK_DRAG')
            add(kmn, v + 'select_box',
                'LEFTMOUSE shift CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'ADD'))
            add(kmn, v + 'select_box',
                'LEFTMOUSE shift ctrl CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'SUB'))
            add(kmn, v + 'select_circle',
                'LEFTMOUSE alt CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'ADD'))
            add(kmn, v + 'select_circle',
                'LEFTMOUSE ctrl alt CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'SUB'))
            add(kmn, v + 'select_lasso',
                'LEFTMOUSE shift alt CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'ADD'))
            add(kmn, v + 'select_lasso',
                'LEFTMOUSE shift ctrl alt CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'SUB'))
        add('View3D Gesture Circle', 'SUBTRACT', 'LEFT_BRACKET alt')
        add('View3D Gesture Circle', 'SUBTRACT', 'LEFT_BRACKET ctrl alt')
        add('View3D Gesture Circle', 'ADD', 'RIGHT_BRACKET alt')
        add('View3D Gesture Circle', 'ADD', 'RIGHT_BRACKET ctrl alt')

        # select tools
        for kmn, v in {
            '3D View Tool: Select ': 'view3d.',
            'Image Editor Tool: Uv, Select ': 'uv.',
            'Node Tool: Select ': 'node.',
        }.items():
            for tool, id in {
                'Box': 'select_box',
                'Circle': 'select_circle',
                'Lasso': 'select_lasso'
            }.items():
                for t in ['', ' (fallback)']:
                    # intersect
                    if kmn == '3D View Tool: Select ' and tool != 'Circle':
                        add(kmn + tool + t, {v + id: {'mode': 4}},
                            'LEFTMOUSE alt CLICK_DRAG', disableOldExactProps='LEFTMOUSE shift ctrl CLICK_DRAG')

        # select
        add('3D View', {'view3d.select': {'center': True, 'object': True, 'toggle': True}},
            'LEFTMOUSE ctrl CLICK', disableOld='LEFTMOUSE ctrl CLICK')
        add('Object Mode', 'object.select_pattern', 'F ctrl')
        add('Object Mode', 'object.select_by_type', 'T shift')
        add('Object Mode', 'object.select_random', 'R shift')

        for kmn, v in {
            'Markers': 'marker.',
            'Dopesheet': 'action.select_all',
            'Grease Pencil Stroke Edit Mode': 'gpencil.',
            'Grease Pencil Stroke Paint Mode': 'gpencil.',
            'Grease Pencil Stroke Vertex Mode': 'gpencil.',
            'Paint Face Mask (Weight, Vertex, Texture)': 'paint.face_',
            'Paint Vertex Selection (Weight, Vertex)': 'paint.vert_',
            'Pose': 'pose.',
            'Object Mode': 'object.',
            'Curve': 'curve.',
            'Curves': 'curves.',
            'Mesh': 'mesh.',
            'Armature': 'armature.',
            'Metaball': 'mball.',
            'Lattice': 'lattice.',
            'Particle': 'particle.',
            'Sculpt Curves': 'curves.',
            'Animation Channels': 'anim.channels_',
            'UV Editor': 'uv.',
            'Mask Editing': 'mask.',
            'Graph Editor': 'graph.',
            'Node Editor': 'node.',
            'Info': 'info.',
            'File Browser Main': 'file.',
            'NLA Editor': 'nla.',
            'Sequencer': 'sequencer.',
            'SequencerPreview': 'sequencer.',
            'Clip Editor': 'clip.',
            'Clip Graph Editor': 'clip.graph_',  # _markers
            'Outliner': 'outliner.'
        }.items():
            add(kmn, v + 'select_all' + ('_markers' if kmn == 'Clip Graph Editor' else ''),
                'A DOUBLE_CLICK', disableOld='A', setKmiProps=lambda kmi: setActionProp(kmi, 'SELECT'))
            add(kmn, v + 'select_all' + ('_markers' if kmn == 'Clip Graph Editor' else ''),
                'A CLICK', disableOld='A alt', setKmiProps=lambda kmi: setActionProp(kmi, 'DESELECT'))
            add(kmn, v + 'select_all' + ('_markers' if kmn == 'Clip Graph Editor' else ''),
                'A alt', disableOld='I ctrl', setKmiProps=lambda kmi: setActionProp(kmi, 'INVERT'))
            disable(kmn, {v + 'select_all' + ('_markers' if kmn == 'Clip Graph Editor' else ''): {'action': 2}},
                    'A DOUBLE_CLICK')

        for kmn, v in {
            'Pose': 'pose.',
            'Object Mode': 'object.',
            'Armature': 'armature.',
        }.items():
            add(kmn, {v + 'select_hierarchy': {'extend': False}},
                'EQUAL alt', disableOld='LEFT_BRACKET', setKmiProps=lambda kmi: setDirectionProp(kmi, 'PARENT'))
            add(kmn, {v + 'select_hierarchy': {'extend': True}},
                'EQUAL shift', disableOld='LEFT_BRACKET shift', setKmiProps=lambda kmi: setDirectionProp(kmi, 'PARENT'))
            add(kmn, {v + 'select_hierarchy': {'extend': False}},
                'MINUS alt', disableOld='RIGHT_BRACKET', setKmiProps=lambda kmi: setDirectionProp(kmi, 'CHILD'))
            add(kmn, {v + 'select_hierarchy': {'extend': True}},
                'MINUS shift', disableOld='RIGHT_BRACKET shift', setKmiProps=lambda kmi: setDirectionProp(kmi, 'CHILD'))

        # object
        for kmn, v in {
            'Object Mode': 'VIEW3D_MT_object_context_menu',
            'Mesh': 'VIEW3D_MT_edit_mesh_context_menu',
            'Curve': 'VIEW3D_MT_edit_curve_context_menu',
            'UV Editor': 'IMAGE_MT_uvs_context_menu',
            'Graph Editor': 'GRAPH_MT_context_menu',
            'Node Editor': 'NODE_MT_context_menu'
        }.items():
            add(kmn, {'wm.call_menu': {'name': v}},
                'RIGHTMOUSE CLICK', disableOld='RIGHTMOUSE')

        add('Object Mode', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_light_add'}},
            'RIGHTMOUSE alt CLICK')
        add('Object Mode', 'view3d.cursor3d',
            'RIGHTMOUSE shift alt')
        add('Object Mode', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_light_add'}},
            'RIGHTMOUSE shift alt RELEASE')
        add('Object Mode', {'wm.context_enum_menu': {'data_path': 'object.data.energy'}},
            'E')

        add('Object Mode', 'object.empty_add',
            'ACCENT_GRAVE A repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'PLAIN_AXES'), head=True)
        add('Object Mode', {'wm.call_menu': {'name': 'VIEW3D_MT_mesh_add'}},
            'ONE A repeat', head=True)
        for kmn in ['Object Mode', 'Mesh']:
            add(kmn, 'mesh.primitive_plane_add',
                'TWO A repeat', head=True)
            add(kmn, 'mesh.primitive_cube_add',
                'THREE A repeat', head=True)
        add('Object Mode', 'object.load_background_image',
            'FOUR A repeat', head=True)
        add('Object Mode', 'curve.primitive_bezier_curve_add',
            'FIVE A repeat', head=True)
        add('Object Mode', 'object.add',
            'SIX A repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'LATTICE'), head=True)
        add('Object Mode', 'object.add',
            'SEVEN A repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'FONT'), head=True)
        add('Object Mode', 'object.add',
            'ZERO A repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'CAMERA'), head=True)
        add('Object Mode', 'object.add',
            'SPACE A repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'CAMERA'), head=True)

        add('Object Mode', 'object.convert',
            'C shift ctrl CLICK', setKmiProps=lambda kmi: setTargetProp(kmi, 'MESH'))
        add('Object Mode', 'object.convert',
            'LEFTMOUSE shift ctrl C')

        for kmn, v in {
            'Window': 'TOPBAR_PT_name',
            'Markers': 'TOPBAR_PT_name_marker'
        }.items():
            add(kmn, {'wm.call_panel': {'name': v, 'keep_open': False}},
                'R ctrl')
            add(kmn, {'wm.call_panel': {'name': v, 'keep_open': False}},
                'RET CLICK')
        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, 'wm.batch_rename',
                'R ctrl alt')
        add('Outliner', {'outliner.item_rename': {'use_active': True}},
            'R ctrl')
        add('Outliner', {'outliner.item_rename': {'use_active': True}},
            'RET CLICK')

        for kmn, v in {
            'Property Editor': 'constraint.copy',
            'Markers': 'marker.duplicate',
            'Dopesheet': 'action.duplicate_move',
            'Grease Pencil Stroke Edit Mode': 'gpencil.duplicate_move',
            'Object Mode': 'object.duplicate_move',
            'Outliner': 'object.duplicate',
            'Curve': 'curve.duplicate_move',
            'Mesh': 'mesh.duplicate_move',
            'Armature': 'armature.duplicate_move',
            'Metaball': 'mball.duplicate_move',
            'Mask Editing': 'mask.duplicate_move',
            'Graph Editor': 'graph.duplicate_move',
            'Node Editor': 'node.duplicate_move',
            'NLA Editor': 'nla.duplicate_move',
            'Sequencer': 'sequencer.duplicate_move',
        }.items():
            add(kmn, v, 'D ctrl', disableOld='D shift')

        for kmn, v in {
            'Object Mode': 'object.duplicate_move_linked',
            'Node Editor': 'node.duplicate_move_linked',
            'NLA Editor': 'nla.duplicate_linked_move'
        }.items():
            add(kmn, v, 'D ctrl alt', disableOld='D alt')

        add('Outliner', 'object.join',
            'J ctrl')
        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, 'object.join',
                'J CLICK')

        for kmn, v in {
            'Dopesheet': 'action.mirror',
            'Grease Pencil Stroke Edit Mode': 'transform.mirror',
            '3D View': 'transform.mirror',
            'UV Editor': 'transform.mirror',
            'Graph Editor': 'graph.mirror',
        }.items():
            add(kmn, v, 'I ctrl', disableOld='M ctrl')
            add(kmn, v, 'LEFT_ALT ctrl DOUBLE_CLICK', disableOld='M ctrl')

        # object delete
        for kmn, v in {
            'Property Editor': 'constraint.delete',
            'Outliner': 'outliner.delete',
            'Markers': 'marker.delete',
            'Paint Curve': 'paintcurve.delete_point',
            'Object Mode': 'object.delete',
            'Metaball': 'mball.delete_metaelems',
            'Particle': 'particle.delete',
            'Animation Channels': 'anim.channels_delete',
            'Mask Editing': 'mask.delete',
            'Info': 'info.report_delete',
            'File Browser': 'file.delete',
            'NLA Channels': 'nla.tracks_delete',
            'NLA Editor': 'nla.delete',
            'Sequencer': 'sequencer.delete',
            'SequencerPreview': 'sequencer.delete',
            'Clip Editor': 'clip.delete_track',
            'Clip Graph Editor': 'clip.graph_delete_curve',
        }.items():
            add(kmn, v if kmn != 'Object Mode' else {v: {'confirm': False}},
                'X ctrl', disableOld='X')
            add(kmn, v if kmn not in ['Markers', 'Object Mode', 'Metaball', 'Mask Editing', 'Clip Editor', 'Clip Graph Editor'] else {v: {'confirm': False}},
                'BACK_SPACE CLICK', disableOld='DEL')
        add('Object Mode', {'object.select_grouped': {'extend': True}},
            'X shift ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'CHILDREN_RECURSIVE'))
        add('Object Mode', {'object.delete': {'confirm': False}},
            'X shift ctrl RELEASE')

        for kmn, v in {
            'Dopesheet': 'DOPESHEET_MT_delete',
            'Grease Pencil Stroke Edit Mode': 'VIEW3D_MT_edit_gpencil_delete',
            'Grease Pencil Stroke Paint Mode': 'GPENCIL_MT_gpencil_draw_delete',
            'Armature': 'VIEW3D_MT_edit_armature_delete',
            'Graph Editor': 'GRAPH_MT_delete',
        }.items():
            add(kmn, {'wm.call_menu': {'name': v}},
                'X ctrl', disableOld='X')
            if kmn == 'Dopesheet':
                add(kmn, {'action.delete': {'confirm': False}},
                    'BACK_SPACE CLICK', disableOld='DEL')
            elif kmn == 'Graph Editor':
                add(kmn, {'graph.delete': {'confirm': False}},
                    'BACK_SPACE CLICK', disableOld='DEL')
            else:
                add(kmn, {'wm.call_menu': {'name': v}},
                    'BACK_SPACE CLICK', disableOld='DEL')

        for kmn, v in {
            'Grease Pencil Stroke Edit Mode': 'gpencil.active_frames_delete_all',
            'Grease Pencil Stroke Paint Mode': 'gpencil.active_frames_delete_all',
            'Grease Pencil Stroke Sculpt Mode': 'gpencil.active_frames_delete_all',
            'Grease Pencil Stroke Vertex Mode': 'gpencil.active_frames_delete_all',
            'Grease Pencil Stroke Weight Mode': 'gpencil.active_frames_delete_all',
            'Object Mode': 'object.delete',  # 'use_global': True
            'Clip Editor': 'clip.delete_marker',
            'Clip Graph Editor': 'clip.graph_delete_knot',
        }.items():
            if kmn.startswith('Grease Pencil Stroke '):
                add(kmn, v, 'X ctrl alt', disableOld='X shift')
                add(kmn, v, 'BACK_SPACE alt', disableOld='DEL shift')
            elif kmn == 'Object Mode':
                add(kmn, {v: {'use_global': True}},
                    'X ctrl alt', disableOld='X shift')
                add(kmn, {v: {'use_global': True, 'confirm': False}},
                    'BACK_SPACE alt', disableOld='DEL shift')
            else:
                add(kmn, v, 'X ctrl alt', disableOld='X shift')
                add(kmn, {v: {'confirm': False}},
                    'BACK_SPACE alt', disableOld='DEL shift')

        # shade
        add('Object Mode', 'object.shade_smooth',
            'EIGHT')
        add('Object Mode', 'object.shade_smooth',
            'TWO X', head=True)
        add('Object Mode', 'object.shade_flat',
            'EIGHT DOUBLE_CLICK')
        add('Object Mode', 'object.shade_flat',
            'ONE X', head=True)
        add('Object Mode', {'object.shade_smooth': {'use_auto_smooth': True}},
            'EIGHT ctrl')
        add('Object Mode', {'object.shade_smooth': {'use_auto_smooth': True}},
            'THREE X', head=True)

        # linked (select)
        add('Object Mode', 'object.select_linked',
            'E shift')
        add('Outliner', 'outliner.id_operation',
            'E shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'SELECT_LINKED'))
        add('Object Mode', 'object.select_linked',
            'M shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'MATERIAL'))
        add('Object Mode', {'object.select_linked': {'extend': True}},
            'W shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'MATERIAL'))
        add('Object Mode', {'object.select_linked': {'extend': True}},
            'Q shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'OBDATA'))

        # link
        add('Object Mode', {'wm.call_menu': {'name': 'VIEW3D_MT_make_links'}},
            'E ctrl')
        add('Object Mode', 'object.make_links_data',
            'W ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'MATERIAL'))
        add('Object Mode', 'object.make_links_data',
            'Q ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'OBDATA'))
        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, 'object.link_to_collection',
                'L shift ctrl', disableOld='M shift')

        # unlink
        add('Object Mode', {'object.make_single_user': {'object': True, 'obdata': True, 'material': True}},
            'L alt')
        add('Object Mode', {'object.make_single_user': {'object': True, 'obdata': True, 'material': True}},
            'E alt')
        add('Object Mode', {'object.make_single_user': {'material': True}},
            'M alt')
        add('Object Mode', {'object.make_single_user': {'material': True}},
            'W alt')
        add('Object Mode', {'object.make_single_user': {'object': True, 'obdata': True}},
            'Q alt')
        add('Object Mode', {'object.make_single_user': {'object': True, 'obdata': True, 'material': True, 'animation': True, 'obdata_animation': True}},
            'L ctrl alt')

        # parent
        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, {'object.parent_set': {'keep_transform': True}},
                'P shift ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'OBJECT'))
            add(kmn, {'object.parent_set': {'keep_transform': True}},
                'F', setKmiProps=lambda kmi: setTypeProp(kmi, 'OBJECT'))
            add(kmn, 'object.parent_clear',
                'P ctrl alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'CLEAR_KEEP_TRANSFORM'))
            add(kmn, 'object.parent_clear',
                'F alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'CLEAR_KEEP_TRANSFORM'))

        # collection (group)
        disable('Object Mode', 'collection.create', 'G ctrl')
        disable('Object Mode', 'collection.objects_add_active', 'G shift ctrl')
        disable('Object Mode', 'collection.objects_remove_active', 'G shift alt')
        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, 'object.move_to_collection', 'G ctrl', disableOld='M')
            add(kmn, {'object.move_to_collection': {'collection_index': 0, 'is_new': True}},
                'G shift ctrl')
            add(kmn, {'object.move_to_collection': {'collection_index': 0}},
                'G alt')
        add('Object Mode', 'collection.objects_remove',
            'G ctrl alt', disableOld='G alt')

        # group (select)
        add('Object Mode', {'object.select_grouped': {'extend': True}},
            'D shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'CHILDREN_RECURSIVE'))
        add('Outliner', 'outliner.object_operation',
            'D shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'SELECT_HIERARCHY'))
        for kmn in ['Object Mode', 'Outliner']:
            add(kmn, {'object.select_grouped': {'extend': True}},
                'G', setKmiProps=lambda kmi: setTypeProp(kmi, 'COLLECTION'))
            add(kmn, {'object.select_grouped': {'extend': True}},
                'F shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'PARENT'))
            add(kmn, {'object.select_grouped': {'extend': True}},
                'F shift RELEASE', setKmiProps=lambda kmi: setTypeProp(kmi, 'CHILDREN_RECURSIVE'))

    @classmethod
    def addOutlinerHotkeys(cls):
        # view
        add('Outliner', 'outliner.show_active',
            'SPACE', disableOld='PERIOD')
        add('Outliner', 'outliner.show_hierarchy',
            'ZERO')
        add('Outliner', 'outliner.show_hierarchy',
            'ACCENT_GRAVE Z', head=True)
        add('Outliner', {'outliner.show_one_level': {'open': False}},
            'MINUS')
        add('Outliner', {'outliner.show_one_level': {'open': False}},
            'ONE Z', head=True)
        add('Outliner', {'outliner.show_one_level': {'open': True}},
            'EQUAL')
        add('Outliner', {'outliner.show_one_level': {'open': True}},
            'TWO Z', head=True)
        add('Outliner', {'wm.context_menu_enum': {'data_path': 'space_data.display_mode'}},
            'ACCENT_GRAVE repeat')
        add('Outliner', {'wm.call_panel': {'name': 'OUTLINER_PT_filter'}},
            'ACCENT_GRAVE shift repeat')

        # select
        for k in ['ctrl', 'shift']:
            add('Outliner', {'object.select_grouped': {'extend': True}},
                'LEFTMOUSE ' + k + ' DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'CHILDREN_RECURSIVE'))

        # object
        add('Outliner', 'outliner.id_operation',
            'C alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'SINGLE'))
        add('Outliner', 'outliner.id_operation',
            'X alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'UNLINK'))

        # collection (group)
        add('Outliner', 'outliner.collection_objects_select',
            'G shift')
        add('Outliner', 'outliner.collection_new',
            'C shift ctrl', disableOld='C')
        add('Outliner', 'outliner.collection_duplicate',
            'D shift ctrl')
        add('Outliner', {'outliner.delete': {'hierarchy': True}},
            'X shift ctrl')

        for kmn, v in {
            'User Interface': 'anim.driver_button_add',
            'Outliner': 'outliner.drivers_add_selected'
        }.items():
            add(kmn, v,
                'D alt', disableOld='D ctrl')

        for kmn, v in {
            'User Interface': 'anim.driver_button_remove',
            'Outliner': 'outliner.drivers_delete_selected'
        }.items():
            add(kmn, v,
                'D shift alt', disableOld='D ctrl alt')

    @classmethod
    def addTransformationsHotkeys(cls):
        # actions
        add('Window', 'wm.search_menu',
            'SPACE ctrl')
        add('Window', {'wm.call_menu': {'name': 'SCREEN_MT_user_menu'}},
            'SPACE alt', disableOld='Q')
        add('Screen', 'ed.undo_history',
            'Z shift ctrl alt')
        add('Screen', 'screen.repeat_last',
            'Z ctrl alt', disableOld='R shift')

        # tools
        add('3D View', {'wm.tool_set_by_id': {'name': 'builtin.move'}},
            'T')
        add('3D View', {'wm.context_menu_enum': {'data_path': 'scene.transform_orientation_slots[1].type'}},
            'LEFTMOUSE T')

        # transform
        add('Transform Modal Map', 'AXIS_Y',
            'LEFT_ALT')
        add('Transform Modal Map', 'PLANE_Y',
            'LEFT_ALT shift')
        for kmn in [
            'Markers', 'Grease Pencil Stroke Edit Mode',
            '3D View', 'UV Editor', 'Mask Editing',
            'Graph Editor', 'Node Editor', 'SequencerPreview',
            'Clip Editor', 'Clip Graph Editor'
        ]:
            if kmn == 'Markers':
                add(kmn, 'marker.move',
                    'D', disableOld='G')
                add(kmn, {'marker.move': {'tweak': True}},
                    'RIGHTMOUSE CLICK_DRAG', disableOld='LEFTMOUSE CLICK_DRAG')
            else:
                add(kmn, 'transform.translate',
                    'D', disableOld='G')
                add(kmn, 'transform.translate',
                    'RIGHTMOUSE CLICK_DRAG', disableOld='LEFTMOUSE CLICK_DRAG')
        add('Object Mode', {'object.location_clear': {'clear_delta': False}},
            'D alt', disableOld='G alt')
        add('3D View', {'view3d.snap_selected_to_cursor': {'use_offset': True}},
            'Q shift ctrl')
        add('3D View', 'view3d.snap_selected_to_active',
            'D shift ctrl')
        add('Transform Modal Map', 'TRANSLATE',
            'D', disableOld='G')

        # object transform
        add('Object Mode', {'object.transform_apply': {'location': False, 'rotation': True, 'scale': True}},
            'A shift ctrl repeat')
        add('Object Mode', {'object.transform_apply': {'location': True, 'rotation': False, 'scale': False}},
            'X alt repeat')

        for kmn in ['Grease Pencil Stroke Edit Mode', '3D View', 'Mask Editing']:
            add(kmn, 'transform.tosphere',
                'T ctrl', disableOld='S shift alt')
        for kmn in ['Grease Pencil Stroke Edit Mode', '3D View']:
            add(kmn, 'transform.bend',
                'B ctrl', disableOld='W shift')
        add('3D View', 'transform.push_pull',
            'V')
        add('Object Mode', {'object.randomize_transform': {'use_scale': False, 'loc': (0.5, -0.5, 0.0), 'rot': (0.0, 0.0, 0.7854)}},
            'R shift ctrl')

        add('Object Mode', 'object.align',
            'A ctrl alt CLICK')
        add('Object Mode', {'object.align': {'align_axis': 2, 'align_mode': 1}},
            'A ctrl alt DOUBLE_CLICK')
        add('Object Mode', {'object.align': {'align_axis': 1}},
            'X ctrl alt A', head=True)
        add('Object Mode', {'object.align': {'align_axis': 4}},
            'Z ctrl alt A', head=True)

        add('Object Mode', 'transform.transform',
            'T ctrl alt repeat', setKmiProps=lambda kmi: setModeProp(kmi, 'ALIGN'))
        add('Object Mode', 'transform.transform',
            'T alt repeat', setKmiProps=lambda kmi: setModeProp(kmi, 'ALIGN'))

        # orientation
        add('3D View', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_orientations_pie'}},
            'O shift alt', disableOld='COMMA')
        add('3D View', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_orientations_pie'}},
            'LEFT_CTRL shift alt DOUBLE_CLICK')
        add('3D View', {'transform.create_orientation': {'use': True}},
            'COMMA shift ctrl')
        add('3D View', {'transform.create_orientation': {'use': True}},
            'LEFT_ALT shift ctrl DOUBLE_CLICK')
        add('3D View', 'transform.delete_orientation',
            'COMMA ctrl alt')
        add('3D View', 'transform.delete_orientation',
            'LEFT_SHIFT ctrl alt DOUBLE_CLICK')

        # pivot
        for kmn, v in {
            '3D View': 'VIEW3D_MT_pivot_pie',
            'Graph Editor': 'GRAPH_MT_pivot_pie',
            'Image': 'IMAGE_MT_pivot_pie',
            'SequencerPreview': 'SEQUENCER_MT_pivot_pie',
            'Clip Editor': 'CLIP_MT_pivot_pie'
        }.items():
            add(kmn, {'wm.call_menu_pie': {'name': v}},
                'P shift alt', disableOld='PERIOD')
            add(kmn, {'wm.call_menu_pie': {'name': v}},
                'LEFT_SHIFT alt DOUBLE_CLICK')
        add('Object Mode', {'wm.context_toggle': {'data_path': 'tool_settings.use_transform_data_origin'}},
            'V shift', disableOld='PERIOD ctrl')

        add('Object Mode', 'object.origin_set',
            'V alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'ORIGIN_GEOMETRY'))
        add('Object Mode', 'object.origin_set',
            'C alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'ORIGIN_CENTER_OF_VOLUME'))
        add('Object Mode', 'object.origin_set',
            'V shift ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'ORIGIN_CURSOR'))

        # snapping
        add('3D View', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap'}},
            'O', disableOld='TAB shift')
        add('3D View', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap'}},
            'LEFT_CTRL X')
        add('3D View', {'wm.call_panel': {'name': 'VIEW3D_PT_snapping'}},
            'O shift', disableOld='TAB shift ctrl')
        add('3D View', {'wm.call_panel': {'name': 'VIEW3D_PT_snapping'}},
            'LEFT_CTRL shift DOUBLE_CLICK')
        add('3D View', {'wm.context_menu_enum': {'data_path': 'scene.tool_settings.use_snap_project'}},
            'ACCENT_GRAVE X', head=True)

        add('UV Editor', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap_uv'}},
            'O', disableOld='TAB shift')
        add('UV Editor', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap_uv'}},
            'LEFT_CTRL X')
        add('UV Editor', {'wm.call_panel': {'name': 'IMAGE_PT_snapping'}},
            'O shift', disableOld='TAB shift ctrl')
        add('UV Editor', {'wm.call_panel': {'name': 'IMAGE_PT_snapping'}},
            'LEFT_CTRL shift DOUBLE_CLICK')
        disable('UV Editor', {'wm.context_menu_enum': {'data_path': 'tool_settings.snap_uv_element'}},
                'TAB shift ctrl')

        add('Node Editor', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap_node'}},
            'O', disableOld='TAB shift')
        add('Node Editor', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap_node'}},
            'LEFT_CTRL X')
        add('Node Editor', {'wm.context_menu_enum': {'data_path': 'tool_settings.snap_node_element'}},
            'O shift', disableOld='TAB shift ctrl')
        add('Node Editor', {'wm.context_menu_enum': {'data_path': 'tool_settings.snap_node_element'}},
            'LEFT_CTRL shift DOUBLE_CLICK')

        add('Sequencer', {'wm.context_toggle': {'data_path': 'tool_settings.use_snap_sequencer'}},
            'O', disableOld='TAB shift')

        # proportional edit
        for kmn, v in {
            'Dopesheet': 'tool_settings.use_proportional_action',
            'Grease Pencil Stroke Edit Mode': 'tool_settings.use_proportional_edit',
            'Object Mode': 'tool_settings.use_proportional_edit_objects',
            'Curve': 'tool_settings.use_proportional_edit',
            'Curves': 'tool_settings.use_proportional_edit',
            'Mesh': 'tool_settings.use_proportional_edit',
            'Metaball': 'tool_settings.use_proportional_edit',
            'Lattice': 'tool_settings.use_proportional_edit',
            'Particle': 'tool_settings.use_proportional_edit',
            'UV Editor': 'tool_settings.use_proportional_edit',
            'Mask Editing': 'tool_settings.use_proportional_edit_mask',
            'Graph Editor': 'tool_settings.use_proportional_fcurve',
        }.items():
            add(kmn, {'wm.context_toggle': {'data_path': v}},
                'P', disableOld='O')
            add(kmn, {'wm.context_toggle': {'data_path': v}},
                'LEFT_SHIFT X')
            add(kmn, {'wm.call_menu_pie': {'name': 'VIEW3D_MT_proportional_editing_falloff_pie'}},
                'P shift', disableOld='O shift')
            add(kmn, {'wm.call_menu_pie': {'name': 'VIEW3D_MT_proportional_editing_falloff_pie'}},
                'LEFT_ALT shift DOUBLE_CLICK')

            if kmn in ['Grease Pencil Stroke Edit Mode', 'Curve', 'Curves', 'Mesh', 'Metaball', 'UV Editor']:
                add(kmn, {'wm.context_toggle': {'data_path': 'tool_settings.use_proportional_connected'}},
                    'P alt', disableOld='O alt')
                add(kmn, {'wm.context_toggle': {'data_path': 'tool_settings.use_proportional_connected'}},
                    'TAB X', head=True)

    @classmethod
    def addPropertiesHotkeys(cls):
        # modifiers
        add('Object Mode', 'object.modifier_add',
            'SPACE shift alt')
        for k, modType in {
            'N W': 'WEIGHTED_NORMAL',
            'E W': 'WEIGHTED_NORMAL',
            'T D': 'DATA_TRANSFER',

            'I CLICK': 'MIRROR',
            'W CLICK': 'MIRROR',
            'B CLICK': 'BEVEL',
            'S CLICK': 'SKIN',
            'F S': 'SOLIDIFY',
            'D CLICK': 'DISPLACE',
            'C CLICK': 'CURVE',
            'L CLICK': 'LATTICE',
            'F CLICK': 'LATTICE',
            'W S': 'SHRINKWRAP',
            'D S': 'SIMPLE_DEFORM',
            'D C': 'SURFACE_DEFORM',
            'X CLICK': 'ARRAY',
            'C S': 'SCREW',
            'F W': 'WIREFRAME',

            'R CLICK': 'REMESH',
            'E D': 'DECIMATE',
            'T CLICK': 'TRIANGULATE',

            'L B': 'BOOLEAN',
            'Q CLICK': 'BOOLEAN',
            'G CLICK': 'NODES',
        }.items():
            add('Object Mode', 'object.modifier_add',
                k + ' shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, modType))

        for kmn in ['Object Mode', 'Mesh']:
            for i, n in enumerate(INDEXES):
                if i < 6:
                    add(kmn, {'object.subdivision_set': {'level': i, 'relative': False}},
                        (n if i else 'ACCENT_GRAVE') + ' shift alt CLICK', disableOld=n + ' ctrl')  # subdiv (cycle lvl)

        # actions
        for v in ['object.modifier_copy', 'object.gpencil_modifier_copy', 'object.shaderfx_copy']:
            add('Property Editor', v,
                'D ctrl', disableOld='D shift')
        add('Property Editor', 'constraint.copy',
            'D ctrl', disableOld=True)

        for v in ['object.modifier_remove', 'object.gpencil_modifier_remove', 'object.shaderfx_remove']:
            add('Property Editor', {v: {'report': True}},
                'X ctrl', disableOld='X')
            add('Property Editor', {v: {'report': True}},
                'BACK_SPACE CLICK', disableOld='DEL')
        add('Property Editor', 'constraint.delete',
            'X ctrl', disableOld=True)
        add('Property Editor', 'constraint.delete',
            'BACK_SPACE CLICK', disableOld=True)

    @classmethod
    def addAnimationHotkeys(cls):
        add('Frames', 'screen.animation_play',
            'QUOTE', disableOld='SPACE')
        add('Frames', {'screen.animation_play': {'reverse': True}},
            'SEMI_COLON', disableOld='SPACE shift ctrl')

        for kmn, v in {
            'User Interface': 'anim.keyframe_insert_button',  # all: True
            'Outliner': 'anim.keyframe_insert',
            'Dopesheet': 'action.keyframe_insert',
            'Pose': 'anim.keyframe_insert_menu',
            'Object Mode': 'anim.keyframe_insert_menu',
            'Graph Editor': 'graph.keyframe_insert',
            'Clip Editor': 'clip.keyframe_insert',
        }.items():
            add(kmn, v if kmn != 'User Interface' else {v: {'all': True}},
                'K shift', disableOld='I')

        for kmn, v in {
            'User Interface': 'anim.keyframe_delete_button',  # all: True
            'Outliner': 'anim.keyframe_delete',
            'Pose': 'anim.keyframe_delete_v3d',
            'Object Mode': 'anim.keyframe_delete_v3d',
            'Clip Editor': 'clip.keyframe_delete',
        }.items():
            if kmn == 'User Interface':
                add(kmn, {v: {'all': True}},
                    'K alt', disableOld='I alt')
            elif kmn == 'Object Mode':
                add(kmn, {v: {'confirm': False}},
                    'K alt', disableOld='I alt')
            else:
                add(kmn, v,
                    'K alt', disableOld='I alt')

        add('User Interface', {'anim.keyframe_clear_button': {'all': True}},
            'K shift alt', disableOld='I shift alt')

        for kmn in ['Object Mode', 'Pose']:
            add(kmn, 'anim.keying_set_active_set',
                'K ctrl', disableOld='I shift ctrl alt')

        for kmn, v in {
            'User Interface': 'anim.keyingset_button_add',
            'Outliner': 'outliner.keyingset_add_selected'
        }.items():
            add(kmn, v, 'K shift ctrl', disableOld='K')

        for kmn, v in {
            'User Interface': 'anim.keyingset_button_remove',
            'Outliner': 'outliner.keyingset_remove_selected'
        }.items():
            add(kmn, v, 'K ctrl alt', disableOld='K alt')

    @classmethod
    def addEditMeshHotkeys(cls):
        # mode
        for n in ['ONE', 'TWO', 'THREE']:
            for kmn in ['Mesh', 'UV Editor']:
                disable(kmn, 'mesh.select_mode', n + ' ctrl')
                disable(kmn, 'mesh.select_mode', n + ' shift ctrl')

        for k, v in {
            'V': 'vertices', 'E': 'edges', 'F': 'faces'
        }.items():
            disable('Mesh', 'wm.call_menu', k + ' ctrl')

        # symmetry
        for k in ['X', 'Y', 'Z']:
            add('Window', {'wm.context_toggle': {'data_path': 'object.use_mesh_mirror_' + k.lower()}},
                k + ' DOUBLE_CLICK')
        add('Window', {'wm.context_toggle': {'data_path': 'object.use_mesh_mirror_y'}},
            'LEFT_ALT X')

        # auto merge
        add('Mesh', {'wm.context_toggle': {'data_path': 'scene.tool_settings.use_mesh_automerge'}},
            'J')

        # select
        for kmn, v in {
            'Curve': 'curve.select_similar',
            'Mesh': {'wm.call_menu': {'name': 'VIEW3D_MT_edit_mesh_select_similar'}},
            'Armature': 'armature.select_similar',
            'Metaball': 'mball.select_similar',
            'UV Editor': 'uv.select_similar'
        }.items():
            add(kmn, v, 'S shift', disableOldExactProps='G shift')
        add('Mesh', 'mesh.region_to_loop', 'B shift')
        add('Mesh', 'mesh.loop_to_region', 'R shift')
        add('Mesh', {'wm.call_menu': {'name': 'VIEW3D_MT_edit_mesh_select_by_trait'}},
            'T shift')
        add('Mesh', 'mesh.edges_select_sharp', 'E shift')
        add('Mesh', 'mesh.faces_select_linked_flat', 'F shift')
        add('Mesh', 'mesh.select_nth', 'C shift')

        for kmn, v in {
            'Dopesheet': 'action.select_',
            'Grease Pencil Stroke Edit Mode': 'gpencil.select_',
            'Grease Pencil Stroke Sculpt Mode': 'gpencil.select_',
            'Grease Pencil Stroke Vertex Mode': 'gpencil.select_',
            'Paint Face Mask (Weight, Vertex, Texture)': 'paint.face_select_',
            'Paint Vertex Selection (Weight, Vertex)': 'paint.vert_select_',
            'Object Mode': 'object.select_',
            'Curve': 'curve.select_',
            'Curves': 'curves.select_',
            'Mesh': 'mesh.select_',
            'Armature': 'armature.select_',
            'Lattice': 'lattice.select_',
            'Particle': 'particle.select_',
            'UV Editor': 'uv.select_',
            'Mask Editing': 'mask.select_',
            'Graph Editor': 'graph.select_',
            'Sequencer': 'sequencer.select_',
        }.items():
            for m in ['less', 'more']:
                add(kmn, v + m,
                    ('MINUS' if m == 'less' else 'EQUAL') + ' shift')
                add(kmn, v + m,
                    ('MINUS' if m == 'less' else 'EQUAL'))
        add('Mesh', 'mesh.select_prev_item', 'MINUS alt')
        add('Mesh', 'mesh.select_prev_item', 'MINUS shift alt')
        add('Mesh', 'mesh.loop_multi_select', 'MINUS shift alt RELEASE')
        add('Mesh', 'mesh.select_next_item', 'EQUAL alt')
        add('Mesh', 'mesh.select_next_item', 'EQUAL shift alt')
        add('Mesh', 'mesh.loop_multi_select', 'EQUAL shift alt RELEASE')

        for kmn, v in {
            'Pose': 'pose.select_mirror',
            'Mesh': {'mesh.select_mirror': {'extend': True}},
            'Armature': {'armature.select_mirror': {'extend': False}}
        }.items():
            add(kmn, v, 'I shift', disableOld='M shift ctrl')

        for k, v in {
            'X': 1,
            'LEFT_ALT': 2,
            'Z': 4,
        }.items():
            add('Mesh', {'mesh.select_mirror': {'extend': True, 'axis': v}},
                k + ' W', head=True)

        for kmn, v in {
            'Grease Pencil Stroke Edit Mode': 'gpencil.select_linked',
            'Grease Pencil Stroke Sculpt Mode': 'gpencil.select_linked',
            'Grease Pencil Stroke Vertex Mode': 'gpencil.select_linked',
            'Paint Face Mask (Weight, Vertex, Texture)': 'paint.face_select_linked',
            'Paint Vertex Selection (Weight, Vertex)': 'paint.vert_select_linked',
            'Curve': 'curve.select_linked',
            'Curves': 'curves.select_linked',
            'Mesh': 'mesh.select_linked',
            'Armature': 'armature.select_linked',
            'Particle': 'particle.select_linked',
            'UV Editor': 'uv.select_linked',
            'Mask Editing': 'mask.select_linked',
            'Sequencer': 'sequencer.select_linked'
        }.items():
            add(kmn, v, 'L shift', disableOldExactProps='L ctrl')
            if kmn in [
                'Mesh',
                'Curve',
                'Paint Face Mask (Weight, Vertex, Texture)',
                'Paint Vertex Selection (Weight, Vertex)',
                'UV Editor'
            ]:
                add(kmn, v, 'W shift')

        for kmn, v in {
            'Paint Face Mask (Weight, Vertex, Texture)': {'paint.face_select_linked_pick': {'deselect': True}},
            'Paint Vertex Selection (Weight, Vertex)': {'paint.vert_select_linked_pick': {'select': False}},
            'Curve': {'curve.select_linked_pick': {'deselect': True}},
            'Mesh': {'mesh.select_linked_pick': {'deselect': True}},
            'Armature': {'armature.select_linked_pick': {'deselect': True}},
            'Particle': {'particle.select_linked_pick': {'deselect': True}},
            'UV Editor': {'uv.select_linked_pick': {'deselect': True}},
            'Mask Editing': {'mask.select_linked_pick': {'deselect': True}},
        }.items():
            add(kmn, v, 'L DOUBLE_CLICK', disableOld='L shift')
            add(kmn, v, 'W alt')

        # mesh
        for kmn, v in {
            'Mesh': 'VIEW3D_MT_edit_mesh_merge',
            'UV Editor': 'IMAGE_MT_uvs_merge'
        }.items():
            add(kmn, {'wm.call_menu': {'name': v}},
                'M shift', disableOld='M')

        add('Mesh', 'mesh.merge',
            'M', setKmiProps=lambda kmi: setTypeProp(kmi, 'CENTER'))
        add('Mesh', 'mesh.merge',
            'V shift DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'CENTER'))
        add('Mesh', 'mesh.merge',
            'M ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'LAST'))
        add('Mesh', 'mesh.merge',
            'V shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'LAST'))
        add('Mesh', 'mesh.merge',
            'C shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'COLLAPSE'))
        add('Mesh', {'mesh.remove_doubles': {'threshold': 0.001}},
            'M shift alt')
        add('Mesh', {'mesh.remove_doubles': {'threshold': 0.001}},
            'V shift alt')

        for kmn, v in {
            'Mesh': 'mesh.split',
            'Curve': 'curve.split',
            'Armature': 'armature.split',
            'UV Editor': 'uv.select_split',
            'NLA Editor': 'nla.split',
            'Grease Pencil Stroke Edit Mode': 'gpencil.stroke_split'
        }.items():
            add(kmn, v, 'Q alt', disableOld='Y')

        for kmn, v in {
            'Grease Pencil Stroke Edit Mode': 'gpencil.stroke_separate',
            'Mesh': 'mesh.separate',
            'Armature': 'armature.separate',
            'Node Editor': 'node.group_separate',
            'Curve': 'curve.separate'
        }.items():
            add(kmn, v, 'J alt', disableOld='P')
        add('Sequencer', 'sequencer.images_separate', 'J alt', disableOld='Y')

        add('Mesh', 'mesh.separate',
            'J ctrl alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'SELECTED'))
        add('Mesh', 'mesh.separate',
            'A ctrl alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'SELECTED'))
        add('Curve', {'curve.separate': {'confirm': False}},
            'J ctrl alt')
        add('Curve', {'curve.separate': {'confirm': False}},
            'A ctrl alt')

        add('Mesh', 'mesh.separate',
            'J shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'LOOSE'))
        add('Mesh', 'mesh.separate',
            'A shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'LOOSE'))

        # mesh delete
        add('Mesh', {'wm.call_menu': {'name': 'VIEW3D_MT_edit_mesh_delete'}},
            'X shift', disableOld='X')
        disable('Mesh', {'wm.call_menu': {'name': 'VIEW3D_MT_edit_mesh_delete'}},
                'DEL')
        add('Mesh', 'mesh.dissolve_mode',
            'BACK_SPACE CLICK', disableOld='DEL ctrl')
        add('Mesh', 'mesh.dissolve_edges', 'X alt')
        add('Mesh', 'mesh.dissolve_limited', 'X ctrl alt')

        add('Mesh', 'mesh.delete',
            'X shift ctrl CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'FACE'))
        add('Mesh', 'mesh.delete',
            'LEFTMOUSE shift ctrl X')

        add('Mesh', 'mesh.delete', 'BACK_SPACE shift')
        add('Mesh', 'mesh.delete_loose', 'X shift alt')

        # connect
        add('Mesh', 'mesh.vert_connect_path', 'P shift ctrl', disableOld='J')
        add('Mesh', 'mesh.vert_connect_path', 'Q shift')
        add('Mesh', 'mesh.bridge_edge_loops', 'B shift ctrl')
        add('Mesh', 'mesh.bridge_edge_loops', 'F alt')
        add('Mesh', 'mesh.fill', 'F ctrl', disableOld='F alt')
        add('Mesh', 'mesh.fill_grid', 'F shift ctrl')
        add('Mesh', 'mesh.symmetrize',
            'W shift alt repeat')
        add('Mesh', {'mesh.fill_holes': {'sides': 0}},
            'F shift alt repeat')

        for kmn in ['Mesh', 'Curve', 'Lattice']:
            add(kmn, {'wm.call_menu': {'name': 'VIEW3D_MT_hook'}},
                'H shift ctrl', disableOld='H ctrl')

        # divide
        add('Mesh', 'mesh.subdivide', 'D ctrl alt')
        add('Mesh', 'mesh.quads_convert_to_tris',
            'T ctrl alt', disableOld='T ctrl', setKmiProps=lambda kmi: setQuadAndNgonMethodProp(kmi, 'BEAUTY', 'BEAUTY'))
        add('Mesh', 'mesh.quads_convert_to_tris',
            'T alt', disableOld='T shift ctrl')
        add('Mesh', 'mesh.tris_convert_to_quads',
            'T alt DOUBLE_CLICK')
        add('Mesh', 'mesh.poke', 'P ctrl alt')
        add('Mesh', 'mesh.poke', 'V alt')
        add('Mesh', 'mesh.intersect', 'K ctrl alt repeat')
        add('Mesh', 'mesh.intersect',
            'V ctrl repeat', setKmiProps=lambda kmi: setIntersectProps(kmi, 'SELECT', 'NONE'))

        # combine
        add('Mesh', 'mesh.unsubdivide', 'D shift alt')
        add('Mesh', 'mesh.tris_convert_to_quads',
            'Q shift alt', disableOld='J alt')

        # mesh normals
        add('Mesh', {'wm.call_menu': {'name': 'VIEW3D_MT_edit_mesh_normals'}},
            'N shift', disableOld='N alt')
        add('Mesh', 'mesh.flip_normals', 'N')
        add('Mesh', {'mesh.normals_make_consistent': {'inside': False}},
            'N alt', disableOld='N shift')
        add('Mesh', {'mesh.normals_make_consistent': {'inside': False}},
            'SPACE X', head=True)
        disable('Mesh', {'mesh.normals_make_consistent': {'inside': True}},
                'N shift ctrl')
        add('Mesh', 'mesh.point_normals', 'N shift ctrl', disableOld='L alt')

        # mesh transforms
        add('Mesh', {'transform.vertex_random': {'offset': -0.1}},
            'R shift ctrl')
        add('Mesh', {'transform.vertex_warp': {'offset_angle': math.radians(15), 'mix': -0.1, 'max': 0.1}},
            'W ctrl')
        add('Mesh', 'mesh.knife_project', 'K ctrl')
        add('Mesh', 'mesh.knife_project', 'LEFTMOUSE C')
        add('Mesh', {'view3d.select': {'object': True, 'center': True, 'deselect_all': True}},
            'LEFTMOUSE ctrl CLICK')
        add('Mesh', {'view3d.select': {'object': True, 'center': True, 'deselect': True}},
            'LEFTMOUSE ctrl DOUBLE_CLICK')

        # tools/operations
        add('Mesh', {'wm.call_menu': {'name': 'VIEW3D_MT_edit_mesh_extrude'}},
            'E ctrl', disableOld='E alt')
        add('Mesh', 'mesh.extrude_region_shrink_fatten',
            'E alt', setKmiProps=lambda kmi: setShrinkFattenUseEvenOffsetProp(kmi, True))
        add('Mesh', {'mesh.inset': {'use_individual': False}}, 'FOUR')
        add('Mesh', {'mesh.inset': {'use_individual': True}},
            'FOUR shift')

        add('Mesh', 'mesh.bevel',
            'B', disableOld='B ctrl', setKmiProps=lambda kmi: setAffectProp(kmi, 'EDGES'))
        add('Bevel Modal Map', 'CONFIRM',
            'SPACE')
        add('Mesh', 'mesh.bevel',
            'B alt', disableOld='B shift ctrl', setKmiProps=lambda kmi: setAffectProp(kmi, 'VERTICES'))

        add('Mesh', {'mesh.loopcut_slide': {'release_confirm': False}},
            'C CLICK', disableOld='R ctrl')

        add('Mesh', {'wm.tool_set_by_id': {'name': 'builtin.knife'}},
            'ONE alt repeat')
        add('Mesh', {'mesh.knife_tool': {'use_occlude_geometry': True, 'only_selected': False}},
            'LEFT_ALT C')
        add('Mesh', {'mesh.knife_tool': {'use_occlude_geometry': False}},
            'LEFT_CTRL C')
        add('Mesh', {'mesh.knife_tool': {'use_occlude_geometry': False, 'only_selected': True}},
            'LEFT_SHIFT C')

        add('Transform Modal Map', 'VERT_EDGE_SLIDE',
            'D DOUBLE_CLICK', disableOld='G')
        disable('Mesh', 'transform.vert_slide', 'V shift')
        add('Mesh', {'mesh.offset_edge_loops_slide': {'release_confirm': False}},
            'D shift', disableOld='R shift ctrl')

        add('Mesh', {'wm.tool_set_by_id': {'name': 'builtin.spin'}},
            'THREE alt repeat')
        for kmn in ['Grease Pencil Stroke Edit Mode', '3D View', 'UV Editor', 'Mask Editing']:
            add(kmn, 'transform.shear',
                'R alt', disableOld='S shift ctrl alt')
        add('Mesh', {'wm.tool_set_by_id': {'name': 'builtin.shear'}},
            'FOUR alt repeat')

        add('Mesh', {'wm.tool_set_by_id': {'name': 'builtin.rip_region'}},
            'TWO alt repeat')
        add('Mesh', 'mesh.rip_move',
            'RIGHTMOUSE alt CLICK_DRAG', disableOld='V alt', setKmiProps=lambda kmi: setRipUseFillProp(kmi, False))
        add('Mesh', 'mesh.rip_move',
            'RIGHTMOUSE shift alt CLICK_DRAG', disableOld='V', setKmiProps=lambda kmi: setRipUseFillProp(kmi, True))

        add('Mesh', {'mesh.vertices_smooth': {'factor': 0.5, 'wait_for_input': False}},
            'S shift alt')
        add('Mesh', 'transform.edge_crease',
            'C alt', disableOld='E shift')

        # uv
        for kmn, v in {
            'Mesh': 'mesh.',
            'UV Editor': 'uv.'
        }.items():
            add(kmn, {'wm.call_menu': {'name': 'VIEW3D_MT_uv_map'}},
                'U shift', disableOld='U')
            add(kmn, {v + 'mark_seam': {'clear': False}}, 'U')
            add(kmn, {v + 'mark_seam': {'clear': False}},
                'TWO W', head=True)
            add(kmn, {v + 'mark_seam': {'clear': True}}, 'U DOUBLE_CLICK')
            add(kmn, {v + 'mark_seam': {'clear': True}},
                'ONE W', head=True)
            add(kmn, 'uv.unwrap', 'U ctrl')
            add(kmn, 'uv.unwrap', 'LEFT_CTRL W')

            add(kmn, 'uv.seams_from_islands',
                'U alt CLICK' if kmn == 'Mesh' else 'U alt')
            add(kmn, 'uv.seams_from_islands',
                'THREE W RELEASE', head=True)

            if kmn == 'Mesh':
                add(kmn, 'uv.select_all',
                    'U alt', setKmiProps=lambda kmi: setActionProp(kmi, 'SELECT'))
                add(kmn, 'uv.select_all',
                    'THREE W', setKmiProps=lambda kmi: setActionProp(kmi, 'SELECT'), head=True)

            add(kmn, {'uv.smart_project': {'island_margin': 0.01}},
                'U shift ctrl')
            add(kmn, {'uv.smart_project': {'island_margin': 0.01}},
                'LEFT_SHIFT W')

        add('Mesh', 'uv.cube_project',
            'C W', head=True)
        add('Mesh', {'uv.project_from_view': {'scale_to_bounds': False}},
            'V W', head=True)

        add('Mesh', {'wm.context_menu_enum': {'data_path': 'scene.tool_settings.use_transform_correct_face_attributes'}},
            'F ctrl alt')

        # shade
        add('Mesh', 'mesh.faces_shade_smooth', 'EIGHT')
        add('Mesh', 'mesh.faces_shade_smooth', 'TWO X', head=True)
        add('Mesh', 'mesh.faces_shade_flat', 'EIGHT DOUBLE_CLICK')
        add('Mesh', 'mesh.faces_shade_flat', 'ONE X', head=True)
        add('Mesh', 'mesh.mark_sharp', 'SEVEN')
        add('Mesh', {'mesh.mark_sharp': {'clear': True}}, 'SEVEN DOUBLE_CLICK')

        # vertex groups
        disable('Mesh', {'wm.call_menu': {'name': 'VIEW3D_MT_vertex_group'}},
                'G ctrl')
        for kmn in ['Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']:
            add(kmn, 'object.vertex_group_set_active', 'G shift')
        add('UV Editor', {'wm.call_menu': {'name': 'VIEW3D_MT_vertex_group'}},
            'G shift')
        for kmn in ['Mesh', 'UV Editor']:
            add(kmn, 'object.vertex_group_assign_new', 'G shift ctrl')
            add(kmn, 'object.vertex_group_select', 'G')
            add(kmn, 'object.vertex_group_assign', 'G ctrl')
            add(kmn, 'object.vertex_group_remove_from', 'G alt',
                disableOld='G ctrl alt' if kmn == 'Mesh' else False)
            add(kmn, {'object.vertex_group_remove_from': {'use_all_verts': True}},
                'G alt DOUBLE_CLICK')
            add(kmn, 'object.vertex_group_remove', 'G ctrl alt')

        # overlays
        add('Mesh', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_retopology'}},
            'R ctrl alt repeat')
        add('Mesh', {'wm.context_menu_enum': {'data_path': 'space_data.overlay.retopology_offset'}},
            'R shift alt')
        add('Mesh', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_extra_edge_length'}},
            'V ctrl alt')

    @classmethod
    def addCurvesHotkeys(cls):
        # select
        add('Curve', 'curve.shortest_path_pick',
            'LEFTMOUSE ctrl DOUBLE_CLICK')

        # curve
        add('Curve', 'curve.spline_type_set',
            'LEFTMOUSE shift ctrl C')
        add('Curve', 'curve.spline_type_set',
            'C shift ctrl CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'BEZIER'))

        for kmn, v in {
            'Curve': 'curve.cyclic_toggle',
            'Mask Editing': 'mask.cyclic_toggle'
        }.items():
            add(kmn, v, 'C ctrl', disableOld='C alt')
        add('Curve', 'curve.switch_direction', 'V ctrl')

        # vertex points
        add('Curve', 'curve.handle_type_set',
            'V shift', disableOld='V')
        add('Curve', 'curve.handle_type_set',
            'ONE shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'VECTOR'))
        add('Curve', 'curve.handle_type_set',
            'TWO shift', setKmiProps=lambda kmi: setTypeProp(kmi, 'AUTOMATIC'))
        add('Curve', 'curve.handle_type_set',
            'LEFT_ALT DOUBLE_CLICK', setKmiProps=lambda kmi: setTypeProp(kmi, 'TOGGLE_FREE_ALIGN'))

        for kmn, v in {
            'Curve': 'curve.normals_make_consistent',
            'Armature': 'armature.calculate_roll',
            'Mask Editing': 'mask.normals_make_consistent'
        }.items():
            add(kmn, v, 'R ctrl', disableOld='N shift')

        for kmn, v in {
            'Curve': {'wm.call_menu': {'name': 'VIEW3D_MT_edit_curve_delete'}},
            'Curves': 'curves.delete'
        }.items():
            add(kmn, v, 'X shift', disableOld='X')
            disable(kmn, v, 'DEL')

        add('Curve', 'curve.delete',
            'X shift ctrl', setKmiProps=lambda kmi: setTypeProp(kmi, 'VERT'))
        add('Curve', 'curve.dissolve_verts',
            'BACK_SPACE CLICK', disableOld='DEL ctrl')
        add('Curve', 'transform.tilt', 'T alt', disableOld='T ctrl')
        add('Curve', 'curve.tilt_clear', 'T ctrl alt', disableOld='T alt')
        add('Curve', 'curve.smooth', 'S shift alt')
        add('Curve', 'curve.smooth_radius', 'C alt repeat')

        # segments
        add('Curve', 'curve.subdivide', 'D ctrl alt')
        add('Curve', {'curve.decimate': {'ratio': 0.7}}, 'D shift alt')

        # tools
        add('Curve', {'wm.tool_set_by_id': {'name': 'builtin.draw'}},
            'ONE')

        add('Curve', {'wm.tool_set_by_id': {'name': 'builtin.pen'}},
            'TWO')
        add('3D View Tool: Edit Curve, Curve Pen', {'curve.pen': {'select_point': True, 'move_point': True, 'move_segment': True, 'extrude_point': False}},
            'LEFTMOUSE', disableOld='LEFTMOUSE', setKmiProps=lambda kmi: setCloseSplineProp(kmi, 'OFF'))
        add('Curve Pen Modal Map', 'LINK_HANDLES', 'A ANY')
        add('Curve Pen Modal Map', 'MOVE_ADJACENT',
            'LEFT_CTRL', disableOld='LEFT_CTRL any ANY')
        add('3D View Tool: Edit Curve, Curve Pen', {'curve.pen': {'extrude_point': True, 'insert_point': True, 'close_spline': True}},
            'LEFTMOUSE ctrl', disableOld='LEFTMOUSE ctrl', setKmiProps=lambda kmi: setCloseSplineProp(kmi, 'ON_CLICK'))
        add('3D View Tool: Edit Curve, Curve Pen', {'curve.pen': {'delete_point': True}},
            'LEFTMOUSE alt')

        # overlays
        add('Curve', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_curve_normals'}},
            'V ctrl alt')

    @classmethod
    def addArmatureHotkeys(cls):
        # armature
        add('Armature', 'armature.click_extrude',
            'RIGHTMOUSE ctrl CLICK', disableOld='RIGHTMOUSE ctrl')
        add('Armature', 'armature.switch_direction',
            'D shift', disableOld='F alt')
        add('Armature', 'armature.subdivide',
            'D ctrl alt')
        add('Armature', 'armature.symmetrize',
            'W shift alt')
        add('Armature', {'wm.call_menu': {'name': 'VIEW3D_MT_edit_armature_names'}},
            'R ctrl')

    @classmethod
    def addFontHotkeys(cls):
        for k in ['T', 'F', 'V']:
            add('Font', 'font.text_insert',
                k + ' DOUBLE_CLICK')

    @classmethod
    def addSculptHotkeys(cls):
        # direction
        add('Sculpt', {'wm.context_toggle_enum': {'data_path': 'tool_settings.sculpt.brush.direction'}},
            'LEFTMOUSE ctrl alt CLICK', setKmiProps=lambda kmi: setContextToggleValuesProp(kmi, 'ADD', 'SUBTRACT'))

        # brush
        for kmn, v in {
            'Sculpt': 'VIEW3D_PT_sculpt_context_menu',
            'Vertex Paint': 'VIEW3D_PT_paint_vertex_context_menu',
            'Weight Paint': 'VIEW3D_PT_paint_weight_context_menu',
            'Image Paint': 'VIEW3D_PT_paint_texture_context_menu'
        }.items():
            add(kmn, {'wm.call_panel': {'name': v}},
                'RIGHTMOUSE CLICK', disableOld='RIGHTMOUSE')
            add(kmn, {'wm.call_panel': {'name': 'VIEW3D_PT_tools_brush_settings_advanced'}},
                'W shift')
            add(kmn, {'wm.call_panel': {'name': 'VIEW3D_PT_tools_brush_select'}},
                'B shift')

        for kmn, v in {
            'Sculpt': 'tool_settings.sculpt.brush',
            'Sculpt Curves': 'tool_settings.curves_sculpt.brush',
            'Weight Paint': 'tool_settings.weight_paint.brush',
            'Image Editor Tool: Uv, Sculpt Stroke': 'tool_settings.uv_sculpt.brush'
        }.items():
            add(kmn, {'wm.radial_control': {
                'data_path_primary': v + '.size',
                'data_path_secondary': 'tool_settings.unified_paint_settings.size',
                'use_secondary': 'tool_settings.unified_paint_settings.use_unified_size',
                'rotation_path': v + '.texture_slot.angle',
                'color_path': v + '.cursor_color_add',
                'image_id': v}},
                'E', disableOld='F')
            add(kmn, {'wm.radial_control': {
                'data_path_primary': v + '.strength',
                'data_path_secondary': 'tool_settings.unified_paint_settings.strength',
                'use_secondary': 'tool_settings.unified_paint_settings.use_unified_strength',
                'rotation_path': v + '.texture_slot.angle',
                'color_path': v + '.cursor_color_add',
                'image_id': v}},
                'E shift', disableOld='F shift')
        for kmn, v in {
            'Vertex Paint': 'tool_settings.vertex_paint.brush',
            'Image Paint': 'tool_settings.image_paint.brush',
        }.items():
            add(kmn, {'wm.radial_control': {
                'data_path_primary': v + '.size',
                'data_path_secondary': 'tool_settings.unified_paint_settings.size',
                'use_secondary': 'tool_settings.unified_paint_settings.use_unified_size',
                'rotation_path': v + '.texture_slot.angle',
                'color_path': v + '.cursor_color_add',
                'image_id': v,
                'fill_color_path': v + '.color',
                'fill_color_override_path': 'tool_settings.unified_paint_settings.color',
                'fill_color_override_test_path': 'tool_settings.unified_paint_settings.use_unified_color',
                'zoom_path': '',
                'secondary_tex': True if kmn == 'Image Paint' else False}},
                'E', disableOld='F')
            add(kmn, {'wm.radial_control': {
                'data_path_primary': v + '.strength',
                'data_path_secondary': 'tool_settings.unified_paint_settings.strength',
                'use_secondary': 'tool_settings.unified_paint_settings.use_unified_strength',
                'rotation_path': v + '.texture_slot.angle',
                'color_path': v + '.cursor_color_add',
                'image_id': v,
                'fill_color_path': v + '.color',
                'fill_color_override_path': 'tool_settings.unified_paint_settings.color',
                'fill_color_override_test_path': 'tool_settings.unified_paint_settings.use_unified_color',
                'zoom_path': '',
                'secondary_tex': True if kmn == 'Image Paint' else False}},
                'E shift', disableOld='F shift')
        for kmn, v in {
            'Grease Pencil Stroke Paint Mode': 'tool_settings.gpencil_paint.brush',
            'Grease Pencil Stroke Sculpt Mode': 'tool_settings.gpencil_sculpt_paint.brush',
            'Grease Pencil Stroke Vertex Mode': 'tool_settings.gpencil_vertex_paint.brush',
            'Grease Pencil Stroke Vertex (Draw)': 'tool_settings.gpencil_vertex_paint.brush',
            'Grease Pencil Stroke Vertex (Blur)': 'tool_settings.gpencil_vertex_paint.brush',
            'Grease Pencil Stroke Vertex (Average)': 'tool_settings.gpencil_vertex_paint.brush',
            'Grease Pencil Stroke Vertex (Smear)': 'tool_settings.gpencil_vertex_paint.brush',
            'Grease Pencil Stroke Vertex (Replace)': 'tool_settings.gpencil_vertex_paint.brush',
            'Grease Pencil Stroke Weight Mode': 'tool_settings.gpencil_weight_paint.brush',
            'Particle': 'tool_settings.particle_edit.brush',
        }.items():
            add(kmn, {'wm.radial_control': {'data_path_primary': v + '.size'}},
                'E', disableOld='F')
            if kmn != 'Grease Pencil Stroke Vertex (Replace)':
                cmd = '.gpencil_settings.pen_strength' if kmn != 'Particle' else '.strength'
                add(kmn, {'wm.radial_control': {'data_path_primary': v + cmd}},
                    'E shift', disableOld='F shift')

        add('Sculpt', {'wm.radial_control': {'data_path_primary': 'tool_settings.sculpt.brush.hardness'}},
            'S alt')
        add('Sculpt', {'wm.context_toggle_enum': {'data_path': 'scene.tool_settings.unified_paint_settings.use_locked_size'}},
            'U alt', setKmiProps=lambda kmi: setContextToggleValuesProp(kmi, 'VIEW', 'SCENE'))
        add('Sculpt', {'wm.context_toggle_enum': {'data_path': 'scene.tool_settings.unified_paint_settings.use_locked_size'}},
            'LEFT_ALT DOUBLE_CLICK', setKmiProps=lambda kmi: setContextToggleValuesProp(kmi, 'VIEW', 'SCENE'))

        add('Sculpt', {'wm.context_set_float': {'data_path': 'scene.tool_settings.sculpt.automasking_view_normal_falloff'}},
            'F ctrl alt', setKmiProps=lambda kmi: setValueProp(kmi, 0.0))
        add('Sculpt', {'wm.context_menu_enum': {'data_path': 'scene.tool_settings.sculpt.brush.use_automasking_view_normal'}},
            'F ctrl alt RELEASE')

        # texture
        for kmn, v in {
            'Sculpt': 'tool_settings.sculpt.brush',
        }.items():
            add(kmn, {'wm.call_panel': {'name': 'VIEW3D_PT_tools_brush_texture'}},
                'T shift')
            add(kmn, {'wm.radial_control': {
                'data_path_primary': v + '.texture_slot.angle',
                'rotation_path': v + '.texture_slot.angle',
                'color_path': v + '.cursor_color_add',
                'fill_color_path': '' if kmn == 'Sculpt' else v + '.color',
                'fill_color_override_path': '' if kmn == 'Sculpt' else 'tool_settings.unified_paint_settings.color',
                'fill_color_override_test_path': '' if kmn == 'Sculpt' else 'tool_settings.unified_paint_settings.use_unified_color',
                'image_id': v}},
                'R alt', disableOld='F ctrl')

        # stroke
        for kmn, v in {
            'Sculpt': 'sculpt',
            'Weight Paint': 'weight_paint',
            'Vertex Paint': 'vertex_paint',
            'Image Paint': 'image_paint'
        }.items():
            add(kmn, {'wm.call_panel': {'name': 'VIEW3D_PT_tools_brush_stroke'}},
                'S shift')
            # smooth
            add(kmn, {'wm.context_toggle': {'data_path': 'tool_settings.' + v + '.brush.use_smooth_stroke'}},
                'LEFTMOUSE shift ctrl CLICK', disableOld='S shift')
            add(kmn, {'wm.radial_control': {'data_path_primary': 'tool_settings.' + v + '.brush.smooth_stroke_radius'}},
                'R')
            # method (space(default)/line/curve)
            disable(kmn, {'wm.context_menu_enum': {
                    'data_path': 'tool_settings.' + v + '.brush.stroke_method'}}, 'E')
            add(kmn, {'wm.context_toggle_enum': {'data_path': 'tool_settings.' + v + '.brush.stroke_method'}},
                'LEFTMOUSE alt CLICK', setKmiProps=lambda kmi: setContextToggleValuesProp(kmi, 'LINE', 'SPACE'))
            add(kmn, {'wm.context_toggle_enum': {'data_path': 'tool_settings.' + v + '.brush.stroke_method'}},
                'LEFTMOUSE shift alt CLICK', setKmiProps=lambda kmi: setContextToggleValuesProp(kmi, 'CURVE', 'SPACE'))

        # paint curve
        add('Paint Curve', {'paintcurve.select': {'toggle': True}},
            'A CLICK', disableOld='A')
        add('Paint Curve', {'paintcurve.select': {'toggle': True}},
            'A DOUBLE_CLICK')
        add('Paint Curve', 'paintcurve.add_point_slide',
            'LEFTMOUSE ctrl', disableOld='RIGHTMOUSE ctrl')

        add('Paint Curve', {'paintcurve.slide': {'align': False, 'select': True}},
            'LEFTMOUSE', disableOld='RIGHTMOUSE')
        add('Paint Curve', {'paintcurve.slide': {'align': True, 'select': True}},
            'LEFTMOUSE A', disableOld='RIGHTMOUSE shift', head=True)
        add('Paint Curve', 'transform.translate',
            'RIGHTMOUSE CLICK_DRAG', disableOld='LEFTMOUSE CLICK_DRAG')
        disable('Paint Curve', 'transform.translate', 'G')
        disable('Paint Curve', 'transform.resize', 'S')
        disable('Paint Curve', 'transform.rotate', 'R')
        add('Paint Curve', 'paintcurve.cursor',
            'RIGHTMOUSE shift DOUBLE_CLICK', disableOld='RIGHTMOUSE shift ctrl')

        add('Paint Curve', 'paintcurve.select',
            'LEFTMOUSE alt', disableOld='LEFTMOUSE')
        add('Paint Curve', 'paintcurve.delete_point',
            'LEFTMOUSE alt RELEASE')

        # falloff
        for kmn, v in {
            'Sculpt': 'sculpt',
            'Weight Paint': 'weight_paint',
            'Vertex Paint': 'vertex_paint',
            'Image Paint': 'image_paint'
        }.items():
            add(kmn, {'wm.context_menu_enum': {'data_path': 'tool_settings.' + v + '.brush.curve_preset'}},
                'F shift')
            add(kmn, {'wm.context_menu_enum': {'data_path': 'tool_settings.' + v + '.brush.falloff_shape'}},
                'F ctrl')

        # dyntopo
        add('Sculpt', 'sculpt.dyntopo_detail_size_edit', 'D shift', disableOld='R')
        add('Sculpt', 'sculpt.sample_detail_size',
            'RIGHTMOUSE shift ctrl alt CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'DYNTOPO'))
        disable('Sculpt', 'sculpt.set_detail_size', 'D shift alt')
        add('Sculpt', {'wm.tool_set_by_id': {'name': 'builtin_brush.Simplify'}},
            'D alt')
        add('Sculpt', {'wm.tool_set_by_id': {'name': 'builtin_brush.Slide Relax'}},
            'W')

        # remesh
        add('Sculpt', 'object.voxel_size_edit', 'R shift', disableOld='R')
        add('Sculpt', 'sculpt.sample_detail_size',
            'RIGHTMOUSE shift alt CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'VOXEL'))
        add('Sculpt', {'wm.context_menu_enum': {'data_path': 'object.data.remesh_voxel_size'}},
            'R shift alt')
        disable('Sculpt', 'sculpt.sample_color', 'S')
        add('Sculpt', 'object.voxel_remesh', 'R ctrl')
        add('Sculpt', 'object.quadriflow_remesh', 'F shift ctrl')

        # quick mask
        add('Sculpt', {'paint.mask_box_gesture': {'value': 1.0}},
            'RIGHTMOUSE shift CLICK_DRAG')
        add('Sculpt', {'paint.mask_box_gesture': {'value': 0.0}},
            'RIGHTMOUSE shift ctrl CLICK_DRAG')
        add('Sculpt', {'paint.mask_line_gesture': {'value': 1.0}},
            'RIGHTMOUSE alt CLICK_DRAG')
        disable('Gesture Straight Line', 'CANCEL', 'RIGHTMOUSE any ANY')
        add('Gesture Straight Line', 'SELECT', 'RIGHTMOUSE any RELEASE')
        add('Sculpt', {'paint.mask_line_gesture': {'value': 0.0}},
            'RIGHTMOUSE ctrl alt CLICK_DRAG')
        add('Sculpt', {'paint.mask_lasso_gesture': {'value': 1.0}},
            'RIGHTMOUSE shift alt CLICK_DRAG', disableOld='LEFTMOUSE shift ctrl')
        add('Sculpt', {'paint.mask_lasso_gesture': {'value': 0.0}},
            'RIGHTMOUSE shift ctrl alt CLICK_DRAG')

        # mask
        add('Sculpt', 'paint.brush_select',
            'ONE alt', disableOld='M', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'MASK'))
        add('Sculpt', {'wm.tool_set_by_id': {'name': 'builtin.lasso_mask'}},
            'ONE alt DOUBLE_CLICK')
        add('Sculpt', {'paint.mask_box_gesture': {'value': 0.0, 'use_front_faces_only': True}},
            'B', disableOld='B')
        add('Sculpt', {'paint.mask_box_gesture': {'value': 1.0, 'use_front_faces_only': True}},
            'B ctrl')

        add('Sculpt', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_sculpt_mask_edit_pie'}},
            'Q shift', disableOld='A')
        add('Grease Pencil Stroke Sculpt Mode', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_sculpt_gpencil_automasking_pie'}},
            'Q shift alt', disableOld='A ctrl alt')
        add('Sculpt', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_sculpt_automasking_pie'}},
            'Q shift alt', disableOld='A alt')

        add('Sculpt', {'paint.mask_flood_fill': {'value': 1.0}},
            'Q DOUBLE_CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'VALUE'))
        add('Sculpt', {'paint.mask_flood_fill': {'value': 0.0}},
            'Q', disableOld='M alt', setKmiProps=lambda kmi: setModeProp(kmi, 'VALUE'))
        add('Sculpt', 'paint.mask_flood_fill',
            'Q alt', disableOld='I ctrl', setKmiProps=lambda kmi: setModeProp(kmi, 'INVERT'))

        add('Sculpt', {'sculpt.expand': {'use_mask_preserve': True}},
            'Q ctrl', disableOld='A shift',
            setKmiProps=lambda kmi: setTargetAndFalloffTypeProp(kmi, 'MASK', 'GEODESIC'))
        add('Sculpt', {'sculpt.expand': {'use_mask_preserve': True}},
            'Q shift ctrl', disableOld='A shift alt',
            setKmiProps=lambda kmi: setTargetAndFalloffTypeProp(kmi, 'MASK', 'NORMALS'))

        for k, v in {
            'MINUS shift': 'SHRINK',
            'LEFT_CTRL shift DOUBLE_CLICK': 'SHRINK',
            'EQUAL shift': 'GROW',
            'LEFT_ALT shift DOUBLE_CLICK': 'GROW',

            'MINUS shift ctrl': 'CONTRAST_DECREASE',
            'LEFT_ALT ctrl DOUBLE_CLICK': 'CONTRAST_DECREASE',
            'EQUAL shift ctrl': 'CONTRAST_INCREASE',
            'EQUAL ctrl alt': 'CONTRAST_INCREASE',
            'LEFT_SHIFT ctrl DOUBLE_CLICK': 'CONTRAST_INCREASE',

            'MINUS shift alt': 'SHARPEN',
            'MINUS ctrl alt': 'SHARPEN',
            'LEFT_CTRL alt DOUBLE_CLICK': 'SHARPEN',
            'EQUAL shift alt': 'SMOOTH',
            'LEFT_SHIFT alt DOUBLE_CLICK': 'SMOOTH',
        }.items():
            isAuto = False if 'DOUBLE_CLICK' in k else True
            add('Sculpt', {'sculpt.mask_filter': {'auto_iteration_count': isAuto}},
                k, setKmiProps=lambda kmi: setFilterTypeProp(kmi, v))

        add('Sculpt', {'mesh.paint_mask_extract': {'smooth_iterations': 0, 'add_solidify': False}},
            'D shift ctrl')
        add('Sculpt', {'mesh.paint_mask_slice': {'new_object': True}},
            'D shift alt')
        add('Sculpt', {'mesh.paint_mask_slice': {'new_object': False, 'fill_holes': True}},
            'X shift ctrl repeat')
        add('Sculpt', {'mesh.paint_mask_slice': {'new_object': False, 'fill_holes': False}},
            'X ctrl alt repeat')

        add('Sculpt', {'sculpt.mask_from_cavity': {'mix_factor': 2.0, 'factor': 1.0}},
            'C shift')

        # face sets (areas)
        add('Sculpt', {'wm.tool_set_by_id': {'name': 'builtin_brush.Draw Face Sets'}},
            'TWO alt')
        add('Sculpt', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_sculpt_face_sets_edit_pie'}},
            'A shift', disableOld='W')
        add('Sculpt', {'wm.call_menu': {'name': 'VIEW3D_MT_face_sets_init'}},
            'A shift alt', disableOld='')
        add('Sculpt', 'sculpt.face_sets_create',
            'A DOUBLE_CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'VISIBLE'))
        add('Sculpt', 'sculpt.face_sets_create',
            'A alt', setKmiProps=lambda kmi: setModeProp(kmi, 'MASKED'))
        add('Sculpt', 'sculpt.face_sets_create',
            'W alt', setKmiProps=lambda kmi: setModeProp(kmi, 'SELECTION'))

        add('Sculpt', {'sculpt.expand': {'use_mask_preserve': False, 'use_modify_active': False}},
            'A ctrl', disableOld='W shift',
            setKmiProps=lambda kmi: setTargetAndFalloffTypeProp(kmi, 'FACE_SETS', 'GEODESIC'))
        add('Sculpt', {'sculpt.expand': {'use_mask_preserve': False, 'use_modify_active': True}},
            'A shift ctrl', disableOld='W shift alt',
            setKmiProps=lambda kmi: setTargetAndFalloffTypeProp(kmi, 'FACE_SETS', 'BOUNDARY_FACE_SET'))

        add('Sculpt', 'sculpt.face_set_edit',
            'EQUAL alt', disableOld='W ctrl', setKmiProps=lambda kmi: setModeProp(kmi, 'GROW'))
        add('Sculpt', 'sculpt.face_set_edit',
            'MINUS alt', disableOld='W ctrl alt', setKmiProps=lambda kmi: setModeProp(kmi, 'SHRINK'))

        add('Sculpt', 'sculpt.face_set_change_visibility',
            'H', disableOld='H shift', setKmiProps=lambda kmi: setModeProp(kmi, 'HIDE_ACTIVE'))
        add('Sculpt', 'sculpt.face_set_change_visibility',
            'H shift', setKmiProps=lambda kmi: setModeProp(kmi, 'TOGGLE'))
        disable(
            'Sculpt', {'sculpt.face_set_change_visibility': {'mode': 0}}, 'H')
        add('Sculpt', 'paint.hide_show',
            'H shift ctrl')
        add('Sculpt', 'sculpt.reveal_all',
            'H alt')
        add('Sculpt', 'sculpt.face_set_invert_visibility',
            'H ctrl')

        # quick trim/project
        add('Sculpt', 'sculpt.trim_box_gesture', 'X shift')
        add('Sculpt', 'sculpt.project_line_gesture', 'X alt')
        add('Sculpt', 'sculpt.trim_lasso_gesture', 'X ctrl')

        # modifiers
        for i, n in enumerate(NUMBERS):
            if i < 6:
                add('Sculpt', 'object.modifier_add',
                    n + ' shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'SUBSURF'))  # subdiv
        for i, n in enumerate(INDEXES):
            if i < 6:
                add('Sculpt', {'object.subdivision_set': {'level': i, 'relative': False}},
                    (n if i else 'ACCENT_GRAVE') + ' shift', disableOld=n + ' ctrl')  # multires (default) + cycle subdiv/multires

        # filters
        add('Sculpt', {'wm.tool_set_by_id': {'name': 'builtin.mesh_filter'}},
            'FOUR alt')
        add('Sculpt', 'sculpt.mesh_filter',
            'S shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'SMOOTH'))
        add('Sculpt', 'sculpt.mesh_filter',
            'F shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'INFLATE'))
        add('Sculpt', 'sculpt.mesh_filter',
            'T shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'SHARPEN'))
        add('Sculpt', 'sculpt.mesh_filter',
            'E shift alt', setKmiProps=lambda kmi: setTypeProp(kmi, 'RELAX'))

        # symmetry
        add('Sculpt', {'wm.call_panel': {'name': 'VIEW3D_PT_sculpt_symmetry_for_topbar'}},
            'W shift alt')

        # brushes/tools
        add('Sculpt', 'paint.brush_select',
            'ONE', disableOld='X', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'DRAW'))
        add('Sculpt', 'paint.brush_select',
            'D', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'DRAW_SHARP'))
        add('Sculpt', 'paint.brush_select',
            'C alt', disableOld='C shift', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'CREASE'))
        add('Sculpt', 'paint.brush_select',
            'TWO', disableOld='C', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'CLAY'))
        add('Sculpt', 'paint.brush_select',
            'C', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'CLAY_STRIPS'))
        add('Sculpt', 'paint.brush_select',
            'F alt', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'INFLATE'))
        add('Sculpt', 'paint.brush_select',
            'B alt', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'BLOB'))
        add('Sculpt', 'paint.brush_select',
            'V ctrl', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'LAYER'))

        add('Sculpt', {'paint.brush_select': {'toggle': True, 'create_missing': True}},
            'S', disableOld='S shift', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'SMOOTH'))
        add('Sculpt', 'paint.brush_select',
            'F', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'FILL'))
        add('Sculpt', 'paint.brush_select',
            'F DOUBLE_CLICK', disableOld='T shift', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'FLATTEN'))
        add('Sculpt', 'paint.brush_select',
            'THREE', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'SCRAPE'))
        add('Sculpt', 'paint.brush_select',
            'M', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'MULTIPLANE_SCRAPE'))
        add('Sculpt', 'paint.brush_select',
            'FOUR', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'MULTIPLANE_SCRAPE'))

        add('Sculpt', 'paint.brush_select',
            'G', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'GRAB'))
        add('Sculpt', {'wm.context_menu_enum': {'data_path': 'tool_settings.sculpt.brush.use_grab_silhouette', 'value': False}},
            'G ctrl')
        add('Sculpt', 'paint.brush_select',
            'E alt', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'ELASTIC_DEFORM'))
        add('Sculpt', 'paint.brush_select',
            'E ctrl', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'SNAKE_HOOK'))
        add('Sculpt', 'paint.brush_select',
            'N', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'NUDGE'))
        add('Sculpt', 'paint.brush_select',
            'V', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'PINCH'))
        add('Sculpt', 'paint.brush_select',
            'T alt', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'THUMB'))
        add('Sculpt', 'paint.brush_select',
            'W ctrl', setKmiProps=lambda kmi: setSculptToolProp(kmi, 'ROTATE'))

        add('Sculpt', {'wm.tool_set_by_id': {'name': 'builtin.transform'}},
            'T')
        add('3D View Tool: Transform', 'transform.resize',
            'LEFTMOUSE')
        add('Sculpt', {'wm.context_menu_enum': {'data_path': 'scene.transform_orientation_slots[1].type'}},
            'LEFTMOUSE T')

        # pivot
        add('Sculpt', 'sculpt.set_pivot_position',
            'RIGHTMOUSE shift CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'SURFACE'))
        add('Sculpt', 'sculpt.set_pivot_position',
            'V alt', setKmiProps=lambda kmi: setModeProp(kmi, 'UNMASKED'))
        add('Sculpt', 'sculpt.set_pivot_position',
            'V alt DOUBLE_CLICK', setKmiProps=lambda kmi: setModeProp(kmi, 'ORIGIN'))

        # overlays
        add('Sculpt', {'wm.context_toggle': {'data_path': 'scene.tool_settings.sculpt.show_mask'}},
            'Q ctrl alt', disableOld='M ctrl')
        add('Sculpt', {'wm.context_toggle': {'data_path': 'space_data.overlay.show_sculpt_face_sets'}},
            'A ctrl alt')

    @classmethod
    def addPaintHotkeys(cls):
        # slot
        add('Image Paint', {'wm.call_panel': {'name': 'VIEW3D_PT_slots_projectpaint'}},
            'TAB shift')

        # selection mask
        for kmn, v in {
            'Vertex Paint': 'vertex',
            'Weight Paint': 'weight',
            'Image Paint': 'image'
        }.items():
            add(kmn, {'wm.context_toggle': {'data_path': v + '_paint_object.data.use_paint_mask'}},
                'ONE', disableOld='M')
            if kmn != 'Image Paint':
                add(kmn, {'wm.context_toggle': {'data_path': v + '_paint_object.data.use_paint_mask_vertex'}},
                    'TWO', disableOld='V')

        # blend
        for kmn, v in {
            'Vertex Paint': 'tool_settings.vertex_paint.',
            'Image Paint': 'tool_settings.image_paint.',
        }.items():
            add(kmn, {'wm.context_menu_enum': {'data_path': v + 'brush.blend'}},
                'RIGHTMOUSE ctrl alt CLICK')
            add('Image Paint', {'wm.context_toggle_enum': {'data_path': v + 'brush.blend'}},
                'LEFTMOUSE ctrl alt CLICK', setKmiProps=lambda kmi: setContextToggleValuesProp(kmi, 'ERASE_ALPHA', 'MIX'))

        # brush
        add('Weight Paint', {'wm.radial_control': {
            'data_path_primary': 'tool_settings.weight_paint.brush.weight',
            'data_path_secondary': 'tool_settings.unified_paint_settings.weight',
            'use_secondary': 'tool_settings.unified_paint_settings.use_unified_weight',
            'rotation_path': 'tool_settings.weight_paint.brush.texture_slot.angle',
            'color_path': 'tool_settings.weight_paint.brush.cursor_color_add',
            'image_id': 'tool_settings.weight_paint.brush',
            'secondary_tex': False}},
            'W ctrl', disableOld='F ctrl')
        add('Image Paint', {'wm.context_toggle': {'data_path': 'scene.tool_settings.unified_paint_settings.use_unified_color'}},
            'U')

        # texture
        for kmn, v in {
            'Vertex Paint': 'tool_settings.vertex_paint.brush',
            'Image Paint': 'tool_settings.image_paint.brush',
        }.items():
            add(kmn, {'wm.call_panel': {'name': 'VIEW3D_PT_tools_brush_texture'}},
                'T')
            add(kmn, {'wm.radial_control': {
                'data_path_primary': v + '.texture_slot.angle',
                'rotation_path': v + '.texture_slot.angle',
                'color_path': v + '.cursor_color_add',
                'fill_color_path': '' if kmn == 'Sculpt' else v + '.color',
                'fill_color_override_path': '' if kmn == 'Sculpt' else 'tool_settings.unified_paint_settings.color',
                'fill_color_override_test_path': '' if kmn == 'Sculpt' else 'tool_settings.unified_paint_settings.use_unified_color',
                'image_id': v}},
                'R ctrl', disableOld='F ctrl')
        add('Image Paint', {'wm.call_panel': {'name': 'VIEW3D_PT_tools_mask_texture'}},
            'T shift')
        add('Image Paint', {'wm.radial_control': {
            'data_path_primary': 'tool_settings.image_paint.brush.mask_texture_slot.angle',
            'rotation_path': 'tool_settings.image_paint.brush.mask_texture_slot.angle',
            'color_path': 'tool_settings.image_paint.brush.cursor_color_add',
            'fill_color_path': 'tool_settings.image_paint.brush.color',
            'fill_color_override_path': 'tool_settings.unified_paint_settings.color',
            'fill_color_override_test_path': 'tool_settings.unified_paint_settings.use_unified_color',
            'image_id': 'tool_settings.image_paint.brush',
            'secondary_tex': True}},
            'R alt', disableOld='F ctrl alt')

        # stencil texture
        for kmn in ['Sculpt', 'Vertex Paint']:
            add(kmn, {'brush.stencil_control': {'mode': 0}},
                'RIGHTMOUSE CLICK_DRAG', disableOld='RIGHTMOUSE', head=True)
            add(kmn, {'brush.stencil_control': {'mode': 1}},
                'RIGHTMOUSE shift CLICK_DRAG', disableOld='RIGHTMOUSE shift', head=True)
            add(kmn, {'brush.stencil_control': {'mode': 2}},
                'RIGHTMOUSE alt CLICK_DRAG', disableOld='RIGHTMOUSE ctrl', head=True)
            add(kmn, {'brush.stencil_control': {'mode': 0, 'texmode': 1}},
                'RIGHTMOUSE ctrl CLICK_DRAG', disableOld='RIGHTMOUSE alt', head=True)
            add(kmn, {'brush.stencil_control': {'mode': 1, 'texmode': 1}},
                'RIGHTMOUSE shift ctrl CLICK_DRAG', disableOld='RIGHTMOUSE shift alt', head=True)
            add(kmn, {'brush.stencil_control': {'mode': 2, 'texmode': 1}},
                'RIGHTMOUSE ctrl alt CLICK_DRAG', disableOld='RIGHTMOUSE ctrl alt', head=True)
            add(kmn, {'brush.stencil_reset_transform': {'mask': False}},
                'RIGHTMOUSE shift alt CLICK', head=True)
            add(kmn, {'brush.stencil_reset_transform': {'mask': True}},
                'RIGHTMOUSE shift ctrl alt CLICK', head=True)
        # for Image Paint
        add('Image Paint', {'brush.stencil_control': {'mode': 0}},
            'RIGHTMOUSE ctrl CLICK_DRAG', disableOld='RIGHTMOUSE')
        add('Image Paint', {'brush.stencil_control': {'mode': 1}},
            'RIGHTMOUSE shift ctrl CLICK_DRAG', disableOld='RIGHTMOUSE shift')
        add('Image Paint', {'brush.stencil_control': {'mode': 2}},
            'RIGHTMOUSE ctrl alt CLICK_DRAG', disableOld='RIGHTMOUSE ctrl')
        add('Image Paint', {'brush.stencil_control': {'mode': 0, 'texmode': 1}},
            'RIGHTMOUSE CLICK_DRAG', disableOld='RIGHTMOUSE alt')
        add('Image Paint', {'brush.stencil_control': {'mode': 1, 'texmode': 1}},
            'RIGHTMOUSE shift CLICK_DRAG', disableOld='RIGHTMOUSE shift alt')
        add('Image Paint', {'brush.stencil_control': {'mode': 2, 'texmode': 1}},
            'RIGHTMOUSE alt CLICK_DRAG', disableOld='RIGHTMOUSE ctrl alt')
        add('Image Paint', {'brush.stencil_reset_transform': {'mask': False}},
            'RIGHTMOUSE shift ctrl alt CLICK')
        add('Image Paint', {'brush.stencil_reset_transform': {'mask': True}},
            'RIGHTMOUSE shift alt CLICK')

        # color
        for kmn in ['Vertex Paint', 'Image Paint']:
            add(kmn, 'paint.sample_color',
                'LEFTMOUSE shift CLICK_DRAG', disableOld='S')
            add(kmn, 'paint.sample_color',
                'LEFTMOUSE shift DOUBLE_CLICK')
        add('Weight Paint', {'wm.tool_set_by_id': {'name': 'builtin.sample_weight'}},
            'LEFTMOUSE shift DOUBLE_CLICK')

        for kmn in ['Vertex Paint', 'Image Paint']:
            add(kmn, 'paint.brush_colors_flip',
                'X shift', disableOld='X')
        add('User Interface', {'ui.reset_default_button': {'all': True}},
            'X alt')

        # weights
        add('Weight Paint', 'paint.weight_set',
            'W alt', disableOld='K shift')
        add('Weight Paint', {'wm.call_menu_pie': {'name': 'VIEW3D_MT_wpaint_vgroup_lock_pie'}},
            'L', disableOld='K')

        # mask
        add('Image Paint', {'wm.tool_set_by_id': {'name': 'builtin_brush.Mask'}},
            'ONE alt')
        add('Image Paint', {'wm.call_panel': {'name': 'VIEW3D_PT_mask'}},
            'Q shift')
        add('Image Paint', {'wm.context_toggle': {'data_path': 'scene.tool_settings.image_paint.use_stencil_layer'}},
            'Q ctrl alt')

        # tools
        for kmn in ['Weight Paint', 'Vertex Paint', 'Image Paint']:
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin_brush.Draw'}},
                'D')
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin_brush.Smear'}},
                'V')
        for kmn in ['Weight Paint', 'Vertex Paint']:
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin_brush.Blur'}},
                'S')
        add('Image Paint', {'wm.tool_set_by_id': {'name': 'builtin_brush.Soften'}},
            'S')

        for kmn in ['Weight Paint', 'Vertex Paint']:
            add(kmn, {'wm.tool_set_by_id': {'name': 'builtin_brush.Average'}},
                'V alt')
        add('Weight Paint', {'wm.tool_set_by_id': {'name': 'builtin.gradient'}},
            'G alt')
        add('Image Paint', {'wm.tool_set_by_id': {'name': 'builtin_brush.Fill'}},
            'F')
        add('Vertex Paint', 'paint.vertex_color_set',
            'F DOUBLE_CLICK')
        add('Image Paint', {'wm.tool_set_by_id': {'name': 'builtin_brush.Clone'}},
            'C alt')

    @classmethod
    def addImageAndUvHotkeys(cls):
        # IMAGE
        add('Image Generic', {'image.save_as': {'copy': True}},
            'S ctrl alt', disableOld='S shift alt')
        add('Window', 'image.save_all_modified',
            'S shift ctrl')

        add('Image Generic', 'image.external_edit',
            'E shift ctrl')
        add('Image Generic', 'image.reload',
            'R ctrl alt', disableOld='R alt')

        add('Image Generic', 'image.open',
            'LEFT_CTRL SPACE')
        add('Image Generic', 'image.new',
            'SPACE TAB', head=True)

        add('Image', {'image.invert': {'invert_r': True, 'invert_g': True, 'invert_b': True}},
            'F ctrl alt')
        add('Image', {'image.invert': {'invert_r': True}},
            'ONE ctrl alt')
        add('Image', {'image.invert': {'invert_g': True}},
            'TWO ctrl alt')
        add('Image', {'image.invert': {'invert_b': True}},
            'THREE ctrl alt')
        add('Image', {'image.invert': {'invert_a': True}},
            'FOUR ctrl alt')
        add('Image', 'image.resize', 'R ctrl alt')
        add('Image', {'image.flip': {'use_flip_x': True}},
            'W ctrl')
        add('Image', {'image.flip': {'use_flip_y': True}},
            'W ctrl alt')
        add('Image Generic', 'image.read_viewlayers',
            'X Z', disableOld='R ctrl')
        add('Image Generic', 'image.cycle_render_slot',
            'EQUAL', disableOld='J')
        add('Image Generic', {'image.cycle_render_slot': {'reverse': True}},
            'MINUS', disableOld='J alt')

        # mode
        add('Image', {'wm.context_pie_enum': {'data_path': 'space_data.ui_mode'}},
            'TAB ctrl')

        # UV
        add('UV Editor', {'wm.context_toggle': {'data_path': 'scene.tool_settings.use_uv_select_sync'}},
            'ACCENT_GRAVE CLICK')
        add('UV Editor', {'wm.context_toggle': {'data_path': 'scene.tool_settings.use_uv_select_sync'}},
            'ACCENT_GRAVE alt')
        add('UV Editor', 'mesh.select_all',
            'ACCENT_GRAVE alt RELEASE', setKmiProps=lambda kmi: setActionProp(kmi, 'SELECT'))
        add('UV Editor', {'wm.context_menu_enum': {'data_path': 'scene.tool_settings.uv_sticky_select_mode'}},
            'ACCENT_GRAVE shift')

        add('UV Editor', {'wm.context_menu_enum': {'data_path': 'space_data.uv_editor.lock_bounds'}},
            'B')
        add('UV Editor', {'wm.context_toggle': {'data_path': 'space_data.uv_editor.use_live_unwrap'}},
            'L ctrl')
        add('UV Editor', 'uv.follow_active_quads',
            'F ctrl')

        add('UV Editor', {'uv.pin': {'clear': False}},
            'C', disableOld='P')
        add('UV Editor', {'uv.pin': {'clear': True}},
            'C DOUBLE_CLICK', disableOld='P alt')
        add('UV Editor', 'uv.select_pinned',
            'C shift', disableOld='P shift')
        add('UV Editor', {'uv.select_box': {'pinned': True}},
            'C ctrl', disableOld='B ctrl')

        add('UV Editor', 'uv.select_split',
            'Q alt', disableOld='Y')
        add('UV Editor', 'uv.rip_move',
            'RIGHTMOUSE alt CLICK_DRAG', disableOld='V')
        add('UV Editor', 'uv.weld',
            'V shift')

        add('UV Editor', 'uv.average_islands_scale',
            'A shift ctrl')
        add('UV Editor', {'uv.pack_islands': {'rotate': False, 'margin': 0.01, 'pin': True}},
            'P shift ctrl', setKmiProps=lambda kmi: setRotationMethodProp(kmi, 'CARDINAL'))
        add('UV Editor', {'uv.pack_islands': {'rotate': False, 'margin': 0.01, 'pin': True}},
            'LEFT_SHIFT ctrl DOUBLE_CLICK', setKmiProps=lambda kmi: setRotationMethodProp(kmi, 'CARDINAL'))

        add('UV Editor', {'uv.minimize_stretch': {'iterations': 50}},
            'S shift alt repeat')
        add('UV Editor', 'uv.stitch',
            'D ctrl', disableOld='V alt')

        add('UV Editor', 'uv.align',
            'A ctrl alt CLICK', setKmiProps=lambda kmi: setAxisProp(kmi, 'ALIGN_AUTO'))
        add('UV Editor', {'wm.call_menu': {'name': 'IMAGE_MT_uvs_align'}},
            'LEFTMOUSE ctrl alt A', disableOld='W shift')

        # select
        add('UV Editor', 'mesh.select_all',
            'A ctrl', setKmiProps=lambda kmi: setActionProp(kmi, 'SELECT'))

        # tools
        add('UV Editor', 'uv.snap_cursor',
            'Q DOUBLE_CLICK', setKmiProps=lambda kmi: setTargetProp(kmi, 'ORIGIN'))
        add('Image', 'image.view_cursor_center',
            'Q ctrl', disableOld='C shift')
        add('UV Editor', 'uv.snap_cursor',
            'Q CLICK', setKmiProps=lambda kmi: setTargetProp(kmi, 'SELECTED'))
        add('UV Editor', {'wm.call_panel': {'name': 'IMAGE_PT_uv_cursor'}},
            'RIGHTMOUSE Q')
        add('UV Editor', 'uv.snap_selected',
            'Q shift ctrl', setKmiProps=lambda kmi: setTargetProp(kmi, 'CURSOR'))

        add('UV Editor', {'wm.tool_set_by_id': {'name': 'builtin.transform'}},
            'T')
        add('UV Editor', {'wm.context_menu_enum': {'data_path': 'scene.tool_settings.use_snap_uv_grid_absolute'}},
            'ACCENT_GRAVE X', head=True)

        add('UV Editor', {'wm.tool_set_by_id': {'name': 'builtin_brush.Grab'}},
            'ONE alt')
        add('UV Editor', {'wm.tool_set_by_id': {'name': 'builtin_brush.Relax'}},
            'THREE alt')
        add('UV Editor', {'wm.tool_set_by_id': {'name': 'builtin_brush.Pinch'}},
            'TWO alt')

        # overlays
        add('Image', {'wm.context_toggle': {'data_path': 'space_data.uv_editor.show_texpaint'}},
            'U ctrl alt')
        add('Image', {'wm.context_toggle': {'data_path': 'space_data.uv_editor.show_texpaint'}},
            'V ctrl alt')
        add('UV Editor', {'wm.context_toggle': {'data_path': 'space_data.uv_editor.show_stretch'}},
            'D ctrl alt')
        add('UV Editor', {'wm.context_menu_enum': {'data_path': 'space_data.uv_editor.display_stretch_type'}},
            'D shift alt')

    @classmethod
    def addFileBrowserHotkeys(cls):
        add('File Browser', {'wm.call_panel': {'name': 'FILEBROWSER_PT_display'}},
            'ACCENT_GRAVE CLICK repeat')
        for k, v in {
            'ONE': 'LIST_VERTICAL',
            'TWO': 'LIST_HORIZONTAL',
            'THREE': 'THUMBNAIL'
        }.items():
            add('File Browser', {'wm.context_set_enum': {'data_path': 'space_data.params.display_type'}},
                k, setKmiProps=lambda kmi: setValueProp(kmi, v))
        add('File Browser', {'wm.context_menu_enum': {'data_path': 'space_data.params.display_size'}},
            'THREE DOUBLE_CLICK')
        add('File Browser', {'wm.call_panel': {'name': 'FILEBROWSER_PT_filter'}},
            'ACCENT_GRAVE shift repeat')
        add('File Browser', {'wm.context_toggle': {'data_path': 'space_data.params.use_filter'}},
            'ACCENT_GRAVE alt')

        for kmn, v in {
            'Outliner': 'outliner',
            'File Browser Main': 'file'
        }.items():
            add(kmn, v + '.select_walk',
                'W repeat', setKmiProps=lambda kmi: setDirectionProp(kmi, 'UP'))
            add(kmn, {v + '.select_walk': {'extend': True}},
                'W shift repeat', setKmiProps=lambda kmi: setDirectionProp(kmi, 'UP'))
            add(kmn, v + '.select_walk',
                'S repeat', setKmiProps=lambda kmi: setDirectionProp(kmi, 'DOWN'))
            add(kmn, {v + '.select_walk': {'extend': True}},
                'S shift repeat', setKmiProps=lambda kmi: setDirectionProp(kmi, 'DOWN'))

        add('File Browser', 'file.parent',
            'Q CLICK')
        add('File Browser', 'file.previous',
            'LEFT_BRACKET', disableOld='BACK_SPACE')
        add('File Browser', 'file.previous',
            'Q ctrl')
        add('File Browser', 'file.next',
            'RIGHT_BRACKET', disableOld='BACK_SPACE shift')
        add('File Browser', 'file.next',
            'Q shift ctrl')

        add('File Browser', 'file.rename',
            'R ctrl')
        add('File Browser', 'file.rename',
            'RET')
        add('File Browser', 'file.execute',
            'TAB CLICK')
        add('File Browser', {'file.directory_new': {'confirm': False}},
            'C shift ctrl', disableOld='I')

        add('File Browser', {'wm.call_menu': {'name': 'FILEBROWSER_MT_operations_menu'}},
            'E')

    @classmethod
    def addShaderHotkeys(cls):
        # mode
        add('Node Editor', {'wm.context_pie_enum': {'data_path': 'space_data.shader_type'}},
            'TAB ctrl')

        # slot
        add('Node Editor', {'wm.call_panel': {'name': 'NODE_PT_material_slots'}},
            'TAB shift')

        # node
        add('Node Editor', 'node.translate_attach',
            'D', disableOld='G')
        disable('Node Editor', 'transform.translate',
                'G')
        disable('Node Editor', 'transform.translate',
                'RIGHTMOUSE CLICK_DRAG')

        add('Node Editor', {'node.link_make': {'replace': True}},
            'F alt', disableOld='F shift')

        add('Node Editor', {'node.select': {'extend': True}},
            'RIGHTMOUSE')
        add('Node Editor', {'node.move_detach_links': {'view2d_edge_pan': True}},
            'RIGHTMOUSE CLICK_DRAG')
        disable('Node Editor', 'node.move_detach_links',
                'LEFTMOUSE alt CLICK_DRAG')
        disable('Node Editor', 'node.move_detach_links_release',
                'RIGHTMOUSE alt CLICK_DRAG')

        add('Node Editor', {'node.duplicate_move_keep_inputs': {'keep_inputs': True}},
            'D shift ctrl', disableOld='D shift ctrl')

        add('Node Editor', 'node.mute_toggle',
            'LEFTMOUSE ctrl DOUBLE_CLICK')

        add('Node Editor', 'node.delete',
            'X ctrl', disableOld='X')
        add('Node Editor', 'node.delete',
            'BACK_SPACE CLICK', disableOld='DEL')
        add('Node Editor', {'node.select': {'deselect_all': True}},
            'LEFTMOUSE alt CLICK', disableOld='LEFTMOUSE alt CLICK')
        add('Node Editor', 'node.delete_reconnect',
            'LEFTMOUSE alt DOUBLE_CLICK', disableOld='X ctrl')
        disable('Node Editor', 'node.delete_reconnect', 'DEL ctrl')

        add('Node Editor', 'node.options_toggle',
            'T CLICK')
        add('Node Editor', 'node.hide_socket_toggle',
            'T DOUBLE_CLICK')
        add('Node Editor', 'node.hide_socket_toggle',
            'T alt', disableOld='H ctrl')

        # tweak select
        add('Node Editor', 'node.select_box',
            'LEFTMOUSE shift CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'ADD'))
        add('Node Editor', 'node.select_box',
            'LEFTMOUSE shift ctrl CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'SUB'))
        add('Node Editor', 'node.select_lasso',
            'LEFTMOUSE shift alt CLICK_DRAG', disableOld='LEFTMOUSE ctrl alt CLICK_DRAG', setKmiProps=lambda kmi: setModeProp(kmi, 'ADD'))

        # select
        add('Node Editor', 'node.select_grouped',
            'S shift', disableOld='G shift')
        add('Node Editor', {'node.select_same_type_step': {'prev': False}},
            'EQUAL', disableOld='RIGHT_BRACKET shift')
        add('Node Editor', {'node.select_same_type_step': {'prev': True}},
            'MINUS', disableOld='LEFT_BRACKET shift')
        add('Node Editor', 'node.select_linked_to',
            'EQUAL shift', disableOld='L shift')
        add('Node Editor', 'node.select_linked_from',
            'MINUS shift', disableOld='L')

        # origins/links
        add('Node Editor', 'node.add_reroute',
            'LEFTMOUSE alt CLICK_DRAG', disableOld='RIGHTMOUSE shift CLICK_DRAG')
        add('Node Editor', 'node.links_mute',
            'LEFTMOUSE ctrl CLICK_DRAG', disableOld='RIGHTMOUSE ctrl alt CLICK_DRAG')
        add('Node Editor', 'node.links_cut',
            'RIGHTMOUSE alt CLICK_DRAG', disableOld='RIGHTMOUSE ctrl CLICK_DRAG')

        # frame (block)
        add('Node Editor', 'node.join', 'B CLICK', disableOld='J ctrl')
        add('Node Editor', 'node.parent_set', 'B ctrl', disableOld='P ctrl')
        add('Node Editor', 'node.detach', 'B alt', disableOld='P alt')

        # node group
        add('Node Editor', 'node.group_make',
            'G CLICK', disableOld='G ctrl')
        add('Node Editor', 'node.group_insert',
            'G ctrl')
        add('Node Editor', 'node.group_separate',
            'G alt', disableOld='P')
        add('Node Editor', {'node.group_edit': {'exit': False}},
            'TAB CLICK', disableOld='TAB')
        add('Node Editor', {'node.group_edit': {'exit': True}},
            'Q CLICK', disableOld='TAB ctrl')

        # add
        add('Node Editor', {'wm.call_menu': {'name': 'NODE_MT_category_SH_NEW_GROUP'}},
            'SPACE shift alt')
        add('Node Editor', {'node.add_node': {'use_transform': True}},
            'LEFT_ALT DOUBLE_CLICK repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'ShaderNodeBsdfPrincipled'))
        add('Node Editor', {'node.add_node': {'use_transform': True}},
            'LEFT_SHIFT alt DOUBLE_CLICK repeat', setKmiProps=lambda kmi: setTypeProp(kmi, 'ShaderNodeMath'))
        for k, v in {
            # shader
            'S X': 'ShaderNodeMixShader',
            # input
            'ONE CLICK': 'ShaderNodeValue',
            'X CLICK': 'ShaderNodeMix',
            'THREE CLICK': 'ShaderNodeRGB',
            'C CLICK': 'ShaderNodeVertexColor',
            'C T': 'ShaderNodeTexCoord',
            'TWO CLICK': 'ShaderNodeTexCoord',
            'G CLICK': 'ShaderNodeNewGeometry',
            'B CLICK': 'ShaderNodeBevel',
            'Q CLICK': 'ShaderNodeAmbientOcclusion',
            # texture
            'T CLICK': 'ShaderNodeTexImage',
            'E T': 'ShaderNodeTexEnvironment',
            'E Z': 'ShaderNodeTexEnvironment',
            'N T': 'ShaderNodeTexNoise',
            'Z CLICK': 'ShaderNodeTexNoise',
            'V T': 'ShaderNodeTexVoronoi',
            'V Z': 'ShaderNodeTexVoronoi',
            # color
            'F CLICK': 'ShaderNodeInvert',
            'U CLICK': 'ShaderNodeHueSaturation',
            'J CLICK': 'ShaderNodeRGBCurve',
            'C B': 'ShaderNodeBrightContrast',
            'B C': 'ShaderNodeBrightContrast',
            'R CLICK': 'ShaderNodeValToRGB',
            'R alt': 'ShaderNodeMapRange',
            # vector
            'V CLICK': 'ShaderNodeMapping',
            'N CLICK': 'ShaderNodeNormalMap',
            'B N': 'ShaderNodeBump',
            'N B': 'ShaderNodeBump',
        }.items():
            add('Node Editor', {'node.add_node': {'use_transform': True}},
                k + ' shift repeat', setKmiProps=lambda kmi: setTypeProp(kmi, v))

        add('Node Editor', {'wm.context_toggle': {'data_path': 'scene.eevee.use_gtao'}},
            'Q ctrl alt repeat')  # eevee ao

        # backimage
        disable('Node Editor', 'node.backimage_sample', 'RIGHTMOUSE alt')
        add('Node Editor', {'node.backimage_zoom': {'factor': 0.8}},
            'EQUAL ctrl', disableOld='V')
        add('Node Editor', {'node.backimage_zoom': {'factor': 1.2}},
            'MINUS ctrl', disableOld='V alt')

    @classmethod
    def editOtherAddonsHotkeys(cls):
        CL(bpy.context.preferences.addons)

        # copy attrs {b}
        if 'space_view3d_copy_attributes' in bpy.context.preferences.addons:
            for kmn, v in {
                'Pose': 'VIEW3D_MT_posecopypopup',
                'Object Mode': 'VIEW3D_MT_copypopup'
            }.items():
                edit(kmn, {'wm.call_menu': {'name': v}},
                     'C shift', oldHotkey='C ctrl')
            add('Object Mode', 'object.copy_obj_vis_rot',
                'D shift ctrl DOUBLE_CLICK', space='user')
            add('Object Mode', 'object.copy_obj_mod',
                'A shift alt', space='user')

        # bool tool {b}
        if 'object_boolean_tools' in bpy.context.preferences.addons:
            add('Object Mode', 'object.booltool_auto_difference',
                'ONE ctrl', space='user')
            add('Object Mode', 'object.booltool_auto_union',
                'TWO ctrl', space='user')
            add('Object Mode', 'object.booltool_auto_slice',
                'THREE ctrl', space='user')
            add('Object Mode', 'object.booltool_auto_intersect',
                'FOUR ctrl', space='user')

        # curve edit tools (insert bezier point)
        if 'curve_edit_tools' in bpy.context.preferences.addons:
            add('Curve', 'curve.insert_bezier_spline_point',
                'C', disableOld='I')

        # univ
        if 'UniV' in bpy.context.preferences.addons:
            add('UV Editor', {'uv.univ_crop': {'axis': 0}},
                'C alt repeat')
            add('UV Editor', {'uv.univ_fill': {'axis': 1}},
                'F repeat')
            add('UV Editor', {'uv.univ_fill': {'axis': 2}},
                'F alt repeat')
            add('UV Editor', {'uv.univ_fill': {'axis': 0}},
                'F DOUBLE_CLICK')
            add('UV Editor', {'uv.univ_orient': {'edge_dir': 0}},
                'T alt repeat')

            add('UV Editor', {'uv.univ_rotate': {'rot_dir': 0, 'mode': 0}},
                'X shift CLICK')
            add('UV Editor', {'uv.univ_rotate': {'rot_dir': 1, 'mode': 0}},
                'Z shift CLICK')
            add('UV Editor', {'uv.univ_rotate': {'rot_dir': 0, 'mode': 1}},
                'X shift alt repeat')
            add('UV Editor', {'uv.univ_rotate': {'rot_dir': 1, 'mode': 1}},
                'Z shift alt repeat')
            add('UV Editor', {'uv.univ_flip': {'axis': 0}},
                'X alt')
            add('UV Editor', {'uv.univ_flip': {'axis': 1}},
                'Z alt')
            add('UV Editor', 'uv.univ_distribute',
                'D alt repeat')
            add('UV Editor', 'uv.univ_sort',
                'D alt DOUBLE_CLICK')

            add('UV Editor', 'uv.univ_texel_density_get',
                'LEFT_ALT DOUBLE_CLICK')
            add('UV Editor', {'uv.univ_texel_density_set': {'custom_texel': -1.0}},
                'LEFT_CTRL alt DOUBLE_CLICK')

            add('UV Editor', 'uv.univ_quadrify', 'Q shift repeat')
            add('UV Editor', 'uv.univ_straight', 'F shift repeat')
            add('UV Editor', 'uv.univ_relax', 'R shift repeat')
            add('UV Editor', 'uv.univ_unwrap', 'W shift alt repeat')
            add('UV Editor', 'uv.univ_stitch', 'D shift repeat')
            add('UV Editor', {'uv.univ_stack': {'between_selected': False}},
                'T shift ctrl repeat')
            add('UV Editor', {'uv.univ_stack': {'between_selected': True}},
                'T shift repeat')
            add('UV Editor', 'uv.univ_select_border', 'B shift repeat')

        # node wrangler {b}
        if 'node_wrangler' in bpy.context.preferences.addons:
            add('Node Editor', 'node.nw_add_textures_for_principled',
                'LEFT_SHIFT ctrl DOUBLE_CLICK', space='user')
            # preview
            edit('Node Editor', {'node.nw_preview_node': {'run_in_geometry_nodes': False}},
                 'RIGHTMOUSE alt CLICK', oldHotkey='LEFTMOUSE shift ctrl')
            edit('Node Editor', {'node.nw_preview_node': {'run_in_geometry_nodes': True}},
                 'RIGHTMOUSE alt CLICK', oldHotkey='LEFTMOUSE shift alt')
            edit('Node Editor', 'node.nw_link_out',
                 'ACCENT_GRAVE CLICK', oldHotkey='O')
            edit('Node Editor', {'wm.call_menu': {'name': 'NODE_MT_nw_switch_node_type_menu'}},
                 'S alt', oldHotkey='S shift')
            # link
            edit('Node Editor', {'node.nw_lazy_connect': {'with_menu': False}},
                 'RIGHTMOUSE ctrl CLICK_DRAG', oldHotkey='RIGHTMOUSE alt')
            edit('Node Editor', {'node.nw_lazy_connect': {'with_menu': True}},
                 'RIGHTMOUSE shift CLICK_DRAG', oldHotkey='RIGHTMOUSE shift alt')
            edit('Node Editor', {'wm.call_menu': {'name': 'NODE_MT_nw_link_active_to_selected_menu'}},
                 'F shift ctrl', oldHotkey='BACK_SLASH')
            edit('Node Editor', {'node.nw_link_active_to_selected': {'replace': False, 'use_outputs_names': False, 'use_node_names': False}},
                 'V', oldHotkey='K')
            edit('Node Editor', {'node.nw_link_active_to_selected': {'replace': True, 'use_outputs_names': False, 'use_node_names': False}},
                 'V alt', oldHotkey='K shift')
            edit('Node Editor', {'node.nw_link_active_to_selected': {'replace': False, 'use_outputs_names': True, 'use_node_names': False}},
                 'Y', oldHotkey='SEMI_COLON')
            edit('Node Editor', {'node.nw_link_active_to_selected': {'replace': True, 'use_outputs_names': True, 'use_node_names': False}},
                 'Y alt', oldHotkey='SEMI_COLON shift')
            edit('Node Editor', {'node.nw_link_active_to_selected': {'replace': False, 'use_outputs_names': False, 'use_node_names': True}},
                 'U', oldHotkey='QUOTE')
            edit('Node Editor', {'node.nw_link_active_to_selected': {'replace': True, 'use_outputs_names': False, 'use_node_names': True}},
                 'U alt', oldHotkey='QUOTE shift')
            # mix nodes
            edit('Node Editor', 'node.nw_lazy_mix',
                 'RIGHTMOUSE shift ctrl CLICK_DRAG', oldHotkey='RIGHTMOUSE shift ctrl')
            # selected auto
            edit('Node Editor', 'node.nw_merge_nodes',
                 'M shift ctrl', oldHotkey='ZERO ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'COMMA shift ctrl', oldHotkey='COMMA ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'PERIOD shift ctrl', oldHotkey='PERIOD ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'SLASH shift ctrl', oldHotkey='SLASH ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'EIGHT shift ctrl', oldHotkey='EIGHT ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'MINUS shift ctrl', oldHotkey='MINUS ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'EQUAL shift ctrl', oldHotkey='EQUAL ctrl')
            # selected math
            edit('Node Editor', 'node.nw_merge_nodes',
                 'COMMA shift alt', oldHotkey='COMMA shift ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'PERIOD shift alt', oldHotkey='PERIOD shift ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'SLASH shift alt', oldHotkey='SLASH shift ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'EIGHT shift alt', oldHotkey='EIGHT shift ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'MINUS shift alt', oldHotkey='MINUS shift ctrl')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'EQUAL shift alt', oldHotkey='EQUAL shift ctrl')
            # selected color
            edit('Node Editor', 'node.nw_merge_nodes',
                 'M shift', oldHotkey='ZERO ctrl alt')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'SLASH shift', oldHotkey='SLASH ctrl alt')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'EIGHT shift', oldHotkey='EIGHT ctrl alt')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'MINUS shift', oldHotkey='MINUS ctrl alt')
            edit('Node Editor', 'node.nw_merge_nodes',
                 'EQUAL shift', oldHotkey='EQUAL ctrl alt')
            # set mix/math type
            edit('Node Editor', 'node.nw_batch_change',
                 'M ctrl alt', oldHotkey='ZERO alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'COMMA ctrl alt', oldHotkey='COMMA alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'PERIOD ctrl alt', oldHotkey='PERIOD alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'SLASH ctrl alt', oldHotkey='SLASH alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'EIGHT ctrl alt', oldHotkey='EIGHT alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'MINUS ctrl alt', oldHotkey='MINUS alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'EQUAL ctrl alt', oldHotkey='EQUAL alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'UP_ARROW ctrl alt', oldHotkey='UP_ARROW alt')
            edit('Node Editor', 'node.nw_batch_change',
                 'DOWN_ARROW ctrl alt', oldHotkey='DOWN_ARROW alt')
            # set node value
            edit('Node Editor', 'node.nw_factor',
                 'ONE ctrl alt', oldHotkey='ONE shift ctrl alt')
            edit('Node Editor', 'node.nw_factor',
                 'ZERO ctrl alt', oldHotkey='ZERO shift ctrl alt')
            edit('Node Editor', 'node.nw_factor',
                 'LEFT_ARROW ctrl alt', oldHotkey='LEFT_ARROW shift ctrl alt')
            edit('Node Editor', 'node.nw_factor',
                 'RIGHT_ARROW ctrl alt', oldHotkey='RIGHT_ARROW shift ctrl alt')
            # copy/align/reset/reload
            edit('Node Editor', {'wm.call_menu': {'name': 'NODE_MT_nw_copy_node_properties_menu'}},
                 'C alt', oldHotkey='C shift')
            edit('Node Editor', 'node.nw_align_nodes',
                 'A ctrl', oldHotkey='EQUAL shift')
            edit('Node Editor', 'node.nw_reload_images',
                 'R ctrl alt', oldHotkey='R alt')
            edit('Node Editor', 'node.nw_reset_nodes',
                 'X alt', oldHotkey='BACK_SPACE')
            edit('Node Editor', 'node.nw_bg_reset',
                 'Z alt', oldHotkey='Z')
            # detach/delete
            edit('Node Editor', 'node.nw_detach_outputs',
                 'Q alt', oldHotkey='D shift alt')
            edit('Node Editor', 'node.nw_del_unused',
                 'X shift alt', oldHotkey='X alt')
            # frame (block)
            edit('Node Editor', 'node.nw_frame_selected',
                 'B shift ctrl', oldHotkey='P shift')
            edit('Node Editor', 'node.nw_copy_label',
                 'L', oldHotkey='V shift')
            edit('Node Editor', 'node.nw_clear_label',
                 'L alt', oldHotkey='L alt')
            edit('Node Editor', 'node.nw_modify_labels',
                 'L shift ctrl', oldHotkey='L shift alt')


# KMI PROPS SETTERS


def setTypeProp(kmi, *args): kmi.properties.type = args[0]


def setModeProp(kmi, *args): kmi.properties.mode = args[0]


def setActionProp(kmi, *args): kmi.properties.action = args[0]


def setDirectionProp(kmi, *args): kmi.properties.direction = args[0]


def setTargetProp(kmi, *args): kmi.properties.target = args[0]


def setValueProp(kmi, *args): kmi.properties.value = args[0]


def setAffectProp(kmi, *args): kmi.properties.affect = args[0]


def setAxisProp(kmi, *args): kmi.properties.axis = args[0]


def setRotationMethodProp(kmi, *args): kmi.properties.rotate_method = args[0]


def setFilterTypeProp(kmi, *args): kmi.properties.filter_type = args[0]


def setSpaceTypeProp(kmi, *args): kmi.properties.space_type = args[0]


def setOrientTypeProp(kmi, *args): kmi.properties.orient_type = args[0]


def setRegionTypeProp(kmi, *args): kmi.properties.region_type = args[0]


def setCloseSplineProp(kmi, *args):
    kmi.properties.close_spline_method = args[0]


def setSculptToolProp(kmi, *args):
    kmi.properties.sculpt_tool = args[0]  # ['DRAW', 'DRAW_SHARP', 'CLAY', 'CLAY_STRIPS', 'CLAY_THUMB', 'LAYER', 'INFLATE', 'BLOB', 'CREASE', 'SMOOTH', 'FLATTEN', 'FILL', 'SCRAPE', 'MULTIPLANE_SCRAPE', 'PINCH', 'GRAB', 'ELASTIC_DEFORM', 'SNAKE_HOOK', 'THUMB', 'POSE', 'NUDGE', 'ROTATE', 'TOPOLOGY', 'CLOTH', 'SIMPLIFY', 'MASK', 'PAINT', 'SMEAR', 'DRAW_FACE_SETS'] \


def setRipUseFillProp(kmi, *args):
    kmi.properties.MESH_OT_rip.use_fill = args[0]


def setShrinkFattenUseEvenOffsetProp(kmi, *args):
    kmi.properties.TRANSFORM_OT_shrink_fatten.use_even_offset = args[0]


def setTargetAndFalloffTypeProp(kmi, *args):
    kmi.properties.target = args[0]
    kmi.properties.falloff_type = args[1]


def setContextToggleValuesProp(kmi, *args):
    kmi.properties.value_1 = args[0]
    kmi.properties.value_2 = args[1]


def setQuadAndNgonMethodProp(kmi, *args):
    kmi.properties.quad_method = args[0]
    kmi.properties.ngon_method = args[1]


def setIntersectProps(kmi, *args):
    kmi.properties.mode = args[0]
    kmi.properties.separate_mode = args[1]
