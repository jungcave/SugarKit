from math import pi
import bpy
import bmesh
import bpy_extras
# from mathutils import Matrix
# from uuid import uuid1 as uuid
from types import SimpleNamespace  # SimpleNamespace(**dict)
import platform
import math
import inspect


# / Use list() to duplicate bpy collection [array] to python list
# / Use dict() to duplicate bpy struct {object} to python dict
# / Use SimpleNamespace() istead of dict {object} to get key's value by dot syntax


# / Log Utils


def C(*args):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(
                    override, text=''.join(str(a) for a in args), type="OUTPUT")


def CD(bpy_dict, tabs=0):
    if not bpy_dict:
        return
    C('  ' * tabs, bpy_dict)
    for attrKey in dir(bpy_dict):
        C('  ' + '  ' * tabs, attrKey, ': ', getattr(bpy_dict, attrKey))
    if not tabs:
        C()


def CL(bpy_col, inDetail=False, nameContains=''):
    if not bpy_col:
        return
    C(bpy_col)
    for item in list(bpy_col):
        if not nameContains or (nameContains and item.name and nameContains.lower() in item.name.lower()):
            CD(item, 1) if inDetail else C('  ', item)
    C()


# / Classes Utils

def getClassesFromFileModule(module):
    classes = [
        obj for _, obj in inspect.getmembers(module, inspect.isclass)
        if obj.__module__ == module.__name__
    ]
    return classes


# / Primitives Utils


def toSimpleNameSpace(bpy_dict):
    obj = SimpleNamespace()
    for attrKey in dir(bpy_dict):
        if not attrKey.startswith("__"):
            setattr(obj, attrKey, getattr(bpy_dict, attrKey))
    return obj


def findIn(arr, cb):
    # call: findIn(['A', 'B', 'C'], lambda it: it == 'B')
    for item in arr:
        if cb(item):
            return item
    return None


def getKeyByValueInDict(d, v):
    for key, val in d.items():
        if val == v:
            return key


# / Keymap Utils


addonKeymaps = []


def addAddonKeymapItem(
    keymapName,
    operatorData,
    hotkey,
    setKmiProps=None,
    disableOld=False,
    disableOldExactProps=None,
):
    wmkcs = bpy.context.window_manager.keyconfigs
    km, kmi = newKeymapItem(
        keyconfig=wmkcs.addon,
        keymapName=keymapName,
        operatorData=operatorData,
        keybind=parseKeybindFromHotkeyString(hotkey),
        setKmiProps=setKmiProps,
        disableOld=parseKeybindFromHotkeyString(disableOld),
        disableOldExactProps=parseKeybindFromHotkeyString(
            disableOldExactProps),
    )
    addonKeymaps.append((km, kmi))


def removeAddonKeymapItems():
    for km, kmi in addonKeymaps:
        km.keymap_items.remove(kmi)
    addonKeymaps.clear()


def addActiveKeymapItem(
    keymapName,
    operatorData,
    hotkey,
    setKmiProps=None,
    disableOld=False,
    disableOldExactProps=None,
    head=False
):
    wmkcs = bpy.context.window_manager.keyconfigs
    newKeymapItem(
        keyconfig=wmkcs.active,
        keymapName=keymapName,
        operatorData=operatorData,
        keybind=parseKeybindFromHotkeyString(hotkey),
        setKmiProps=setKmiProps,
        disableOld=parseKeybindFromHotkeyString(disableOld),
        disableOldExactProps=parseKeybindFromHotkeyString(
            disableOldExactProps),
        head=head
    )


def disableActiveKeymapItem(
    keymapName,
    operatorData,
    hotkey=None
):
    wmkcs = bpy.context.window_manager.keyconfigs
    disableKeymapItem(
        wmkcs.active,
        keymapName,
        operatorData,
        parseKeybindFromHotkeyString(hotkey)
    )


def addUserKeymapItem(
    keymap,  # 'name' | obj
    operatorData,
    hotkey,
    setKmiProps=None,
    disableOld=False,
    disableOldExactProps=None
):
    wmkcs = bpy.context.window_manager.keyconfigs
    newKeymapItem(
        keyconfig=wmkcs.user,
        keymapName=keymap,
        operatorData=operatorData,
        keybind=parseKeybindFromHotkeyString(hotkey),
        setKmiProps=setKmiProps,
        disableOld=parseKeybindFromHotkeyString(disableOld),
        disableOldExactProps=parseKeybindFromHotkeyString(disableOldExactProps)
    )


def editUserKeymapItem(
    keymapName,
    operatorData,
    hotkey,
    oldHotkey=None,
    oldHotkeyExactProps=None,
):
    wmkcs = bpy.context.window_manager.keyconfigs
    idName, properties = parseOperatorData(operatorData)

    if oldHotkey == None:
        kmi = wmkcs.user.keymaps[keymapName].keymap_items.find_from_operator(
            idName)
    elif type(oldHotkey) is str or type(oldHotkey) is dict:
        kmi = findKeymapItem(
            wmkcs.user, keymapName, idName, parseKeybindFromHotkeyString(oldHotkey))
    elif oldHotkeyExactProps != None:
        kmi = findKeymapItem(
            wmkcs.user, keymapName, operatorData, parseKeybindFromHotkeyString(oldHotkey))

    editKeymapItemHotkey(kmi, parseKeybindFromHotkeyString(hotkey))


KEYMAP_NAME_SPACES = {"3D View": "VIEW_3D", "Image": "IMAGE_EDITOR", "Node Editor": "NODE_EDITOR",
                      "SequencerCommon": "SEQUENCE_EDITOR", "Clip": "CLIP_EDITOR", "Dopesheet": "DOPESHEET_EDITOR",
                      "Graph Editor": "GRAPH_EDITOR", "NLA Editor": "NLA_EDITOR", "Text": "TEXT_EDITOR",
                      "Console": "CONSOLE", "Info": "INFO", "Outliner": "OUTLINER", "File Browser": "FILE_BROWSER"}
MODIFIERS = ['any', 'shift', 'ctrl', 'alt', 'cmd', 'repeat']
INPUT_VALUES = ['ANY', 'PRESS', 'RELEASE', 'CLICK',
                'DOUBLE_CLICK', 'CLICK_DRAG', 'NOTHING']


def parseKeybindFromHotkeyString(hotkey):  # 'A shift ctrl CLICK' -> {'A': ['shift', 'ctrl', 'CLICK']} \
    if type(hotkey) is str and len(hotkey.split()):
        hotkeySplit = hotkey.split()
        if len(hotkeySplit) == 1:
            return hotkey
        else:
            return {hotkeySplit.pop(0): hotkeySplit}
    else:
        return hotkey


def parseKeymapNameSpace(keymapName):
    name = keymapName
    if keymapName in list(KEYMAP_NAME_SPACES.keys()):
        space = KEYMAP_NAME_SPACES[keymapName]
    else:
        space = 'EMPTY'
    return name, space


def parseOperatorData(operatorData):
    if type(operatorData) is dict:
        idName = list(operatorData.keys())[0]
        properties = operatorData[idName]
    else:
        idName = operatorData
        properties = None
    return idName, properties


def parseKeybindAttrs(keybind):
    if type(keybind) is dict:
        key = list(keybind.keys())[0]
        modifiers = keybind[key]
        any = 'any' in modifiers
        keyModifier = findIn(
            modifiers, lambda it: it not in MODIFIERS and it not in INPUT_VALUES)
        inputValue = findIn(modifiers, lambda it: it in INPUT_VALUES)
        repeat = findIn(modifiers, lambda it: it == 'repeat')
    else:
        key = keybind
        modifiers = []
        any = False
        keyModifier = None
        inputValue = None
        repeat = None
    return key, modifiers, any, keyModifier, inputValue, repeat


def newKeymapItem(
    keyconfig,
    keymapName,
    operatorData,  # 'id/propvalue' | {[id]: {prop1: 1, ...}}
    keybind,  # 'key' | {[key]: ['shift', 'ctrl', 'alt', 'X', 'CLICK']}
    setKmiProps=None,  # def - for non-default operators or enum props set by value
    disableOld=False,  # True - one that found by find_from_operator() | keybind
    disableOldExactProps=None,  # keybind
    head=False
):
    if type(keymapName) is str:
        kmName, space = parseKeymapNameSpace(keymapName)
        km = keyconfig.keymaps.new(name=kmName, space_type=space) if (
            keyconfig.name == 'Blender addon') else keyconfig.keymaps[kmName]
    elif hasattr(keymapName, 'name') and hasattr(keymapName, 'space_type'):
        km = keymapName
        kmName = km.name
        space = km.space_type

    idName, properties = parseOperatorData(operatorData)
    key, modifiers, any, keyModifier, inputValue, repeat = parseKeybindAttrs(
        keybind)

    if disableOld == True:
        kmi = km.keymap_items.find_from_operator(idName)
        if kmi:
            kmi.active = False
    elif type(disableOld) is str or type(disableOld) is dict:
        disableKeymapItem(
            keyconfig,
            kmName,
            idName,
            keybind=disableOld,
        )
    elif disableOldExactProps != None:
        disableKeymapItem(
            keyconfig,
            kmName,
            operatorData,
            keybind=disableOldExactProps,
        )

    if not km.is_modal:
        kmi = km.keymap_items.new(
            idName,
            key,
            inputValue if inputValue else 'PRESS',
            shift=False if any else 'shift' in modifiers,
            ctrl=False if any else 'ctrl' in modifiers,
            alt=False if any else 'alt' in modifiers,
            oskey=False if any else 'cmd' in modifiers,
            any=any,
            key_modifier=keyModifier if keyModifier else 'NONE',
            repeat=True if repeat else False,
            head=head  # puts item on top of its keymap
        )
    else:
        # Modal
        kmi = km.keymap_items.new_modal(
            idName,
            key,
            inputValue if inputValue else 'PRESS',
            shift=False if any else 'shift' in modifiers,
            ctrl=False if any else 'ctrl' in modifiers,
            alt=False if any else 'alt' in modifiers,
            oskey=False if any else 'cmd' in modifiers,
            any=any,
            key_modifier=keyModifier if keyModifier else 'NONE',
            repeat=True if repeat else False,
        )

    if properties and type(properties) is dict:
        for k, v in properties.items():
            kmi.properties[k] = v

    if setKmiProps:
        try:
            setKmiProps(kmi)
        except Exception as er:
            pass

    return (km, kmi)


def disableKeymapItem(
    keyconfig,
    keymapName,  # '*' - in all keymaps
    operatorData,  # '*' - with any id | '*...' - with any id including ... | \
                   # 'id' - with id with any props | {[id]: False} - with id only without props
    keybind=None,
    log=False
):
    if keymapName != '*':  # Compare in specified keymap \
        try:
            km = keyconfig.keymaps[keymapName]
        except Exception as er:
            km = None

        if km and km.keymap_items:
            for kmi in km.keymap_items:
                if compareKeymapItem(kmi, operatorData, keybind, isModal=km.is_modal, log=log):
                    kmi.active = False
    else:  # Compare in all keymaps \
        for km in keyconfig.keymaps:
            for kmi in km.keymap_items:
                if compareKeymapItem(kmi, operatorData, keybind, isModal=km.is_modal, log=log):
                    kmi.active = False


def compareKeymapItem(kmi, operatorData, keybind, isModal, log=False):
    isOpSame = compareKmiWithOperator(kmi, operatorData, isModal, log=log)
    isKeySame = compareKmiWithKeybind(kmi, keybind, log=log)
    return isOpSame and isKeySame


def compareKmiWithOperator(kmi, operatorData, isModal, log=False):
    if type(operatorData) is str:
        if operatorData == '*':
            return True
        elif operatorData.startswith('*'):
            return True if operatorData[1:] in kmi.idname else False

    idName, properties = parseOperatorData(operatorData)

    if not isModal:
        if idName != kmi.idname:
            return False

        compareProps = False if type(operatorData) is str or (
            not properties and not kmi.properties) else True

        if compareProps:
            # Different props presence
            if (properties and not kmi.properties) or (not properties and kmi.properties):
                return False
            # Different props length
            elif len(properties.items()) != len(kmi.properties.items()):
                return False
            # Compare props one by one
            else:
                for k, v in kmi.properties.items():
                    if (k not in properties) or (properties[k] != v):
                        return False
    elif isModal:
        if idName != kmi.propvalue:
            return False

    return True


def compareKmiWithKeybind(kmi, keybind, log=False):
    if not keybind:
        return True

    key, modifiers, any, keyModifier, inputValue, repeat = parseKeybindAttrs(
        keybind)
    different = []

    if kmi.type != key:
        different.append('type')

    if not any and ("SHIFT" not in key) and (kmi.shift and 'shift' not in modifiers) or ('shift' in modifiers and not kmi.shift):
        different.append('shift')
    if not any and ("CTRL" not in key) and (kmi.ctrl and 'ctrl' not in modifiers) or ('ctrl' in modifiers and not kmi.ctrl):
        different.append('ctrl')
    if not any and ("ALT" not in key) and (kmi.alt and 'alt' not in modifiers) or ('alt' in modifiers and not kmi.alt):
        different.append('alt')
    if not any and ("OSKEY" not in key) and (kmi.oskey and 'cmd' not in modifiers) or ('cmd' in modifiers and not kmi.oskey):
        different.append('cmd')

    if hasattr(kmi, 'any') and ((kmi.any and not any) or (any and not kmi.any)):
        different.append('any')

    if hasattr(kmi, 'key_modifier') and kmi.key_modifier != 'NONE' and kmi.key_modifier != keyModifier:
        different.append('keymod')

    if kmi.value != (inputValue if inputValue else 'PRESS'):
        different.append('value')

    return True if not len(different) else False


def findKeymapItem(
    keyconfig,
    keymapName,
    operatorData,
    keybind
):
    try:
        km = keyconfig.keymaps[keymapName]
    except Exception as er:
        km = None
    if km and km.keymap_items:
        for kmi in km.keymap_items:
            if compareKeymapItem(kmi, operatorData, keybind, isModal=km.is_modal):
                return kmi


def editKeymapItemHotkey(kmi, keybind):
    if not kmi:
        return

    key, modifiers, any, keyModifier, inputValue, repeat = parseKeybindAttrs(
        keybind)

    kmi.type = key
    if any:
        kmi.shift = False
        kmi.ctrl = False
        kmi.alt = False
        kmi.oskey = False
        kmi.any = True
    else:
        kmi.shift = 'shift' in modifiers
        kmi.ctrl = 'ctrl' in modifiers
        kmi.alt = 'alt' in modifiers
        kmi.oskey = 'cmd' in modifiers
    kmi.key_modifier = keyModifier if keyModifier else kmi.key_modifier
    kmi.value = inputValue if inputValue else kmi.value
    kmi.repeat = repeat if repeat != None else kmi.repeat


# Keyconf builder


def restoreDefaultKeymaps():
    wmkcs = bpy.context.window_manager.keyconfigs
    # Restore keymaps to default to avoid future collision bugs
    for dkm in wmkcs.default.keymaps:
        dkm.restore_to_default()


def buildNewActiveKeyconfig(name):
    wmkcs = bpy.context.window_manager.keyconfigs
    # Get old keyconfig
    try:
        kc = wmkcs[name.replace(" ", "_")]
    except Exception as er:
        kc = None
    # Remove old keyconfig if exists
    if kc:
        wmkcs.active = kc
        bpy.ops.wm.keyconfig_preset_add(remove_active=True)
    # Create new keyconfig
    bpy.ops.wm.keyconfig_preset_add(name=name)  # and set active
    kc = wmkcs.active
    # Copy all keymaps and keymap items from default keyconfig
    for dkm in wmkcs.default.keymaps:
        km = kc.keymaps.new(
            name=dkm.name,
            space_type=dkm.space_type,
            region_type=dkm.region_type,
            modal=dkm.is_modal
        )
        for kmi in dkm.keymap_items:
            km.keymap_items.new_from_item(kmi)
    return kc


MODIFIERS_AS_STRINGS = {'shift': '⇧', 'ctrl': '⌃', 'alt': '⌥', 'cmd': '⌘'}
KEYMAPS_NOT_TO_DISABLE = ['Generic Gizmo', 'Generic Gizmo Maybe Drag', 'Generic Gizmo Drag',
                          'Generic Gizmo Click Drag', 'Generic Gizmo Select', '3D View Tool: Object, Add Primitive']


def isValueInKmi(kmi, val):
    if not kmi:
        return False
    elif val in MODIFIERS_AS_STRINGS.values() and not kmi.any:
        modKey = getKeyByValueInDict(MODIFIERS_AS_STRINGS, val)
        return getattr(kmi, 'oskey' if modKey == 'cmd' else modKey)
    else:
        return kmi.type.startswith(val.upper()) and kmi.type != 'ANY'


def disableIncludingHotkeysInKeyconfig(
    keyconfig,
    disableIncluding=[],
    excludes=[]
):
    includingAsStrings = []
    excludesAsStrings = []

    for key in disableIncluding:
        if key in MODIFIERS_AS_STRINGS:
            includingAsStrings.append(MODIFIERS_AS_STRINGS[key])
        else:
            includingAsStrings.append(key)

    for hotkey in excludes:
        for k, v in MODIFIERS_AS_STRINGS.items():
            hotkey = hotkey.replace(k, v)
        excludesAsStrings.append(hotkey)

    if keyconfig and keyconfig.keymaps:
        for km in keyconfig.keymaps:
            if km.keymap_items and km.name not in KEYMAPS_NOT_TO_DISABLE:
                for kmi in km.keymap_items:
                    if kmi.active and kmi.map_type in ['KEYBOARD', 'MOUSE', 'NDOF']:
                        kmiString = kmi.to_string()
                        for val in includingAsStrings:
                            if (
                                kmiString not in excludesAsStrings and
                                isValueInKmi(kmi, val) and val in kmiString and
                                hasattr(kmi, 'idname') and kmi.idname
                            ):
                                kmi.active = False


def clearAllInactiveKeymapItemsInKeyconfig(keyconfig):
    if keyconfig and keyconfig.keymaps:
        for km in keyconfig.keymaps:
            if km and km.keymap_items:
                for kmi in list(km.keymap_items):
                    if not kmi.active:
                        km.keymap_items.remove(kmi)


def saveAndExportKeyconfig(filename):
    bpy.ops.wm.save_userpref()
    path = bpy.utils.user_resource('SCRIPTS', path="presets")
    filepath = bpy.path.native_pathsep(path + '/keyconfig/' + filename)
    bpy.ops.preferences.keyconfig_export(filepath=filepath, all=True)


def clearAndSaveKeyconfig(keyconfig, filename):
    clearAllInactiveKeymapItemsInKeyconfig(keyconfig)
    saveAndExportKeyconfig(filename)


# Trim curve modal


def getKeymapFromContext(context, name, keyconfigName="active"):
    wmkcs = context.window_manager.keyconfigs
    if keyconfigName == "active":
        return wmkcs.active.keymaps[name]
    elif keyconfigName == "user":
        return wmkcs.user.keymaps[name]  # == wmkcs['Blender user'].keymaps[name] \
    elif keyconfigName == 'addon':
        return wmkcs.addon.keymaps[name]  # == wmkcs['Blender addon'].keymaps[name] \
    elif keyconfigName == 'default':
        return wmkcs.default.keymaps[name]  # == wmkcs['Blender'].keymaps[name] \
    else:
        try:
            return wmkcs[keyconfigName].keymaps[name]
        except Exception as er:
            return None


def disableActiveKeymapItems(keymap):
    disabledKeymapItemsIds = []
    if keymap and keymap.keymap_items:
        for kmi in keymap.keymap_items:
            if kmi.active:
                kmi.active = False
                disabledKeymapItemsIds.append(kmi.id)
    return disabledKeymapItemsIds


def removeActiveKeymapItems(keymap):
    if keymap and keymap.keymap_items:
        for kmi in list(keymap.keymap_items):
            if kmi.active:
                keymap.keymap_items.remove(kmi)


def unableDisabledKeymapItems(keymap, disabledKeymapItemsIds):
    if keymap and keymap.keymap_items:
        for kmi in keymap.keymap_items:
            if kmi.id in disabledKeymapItemsIds:
                kmi.active = True
        disabledKeymapItemsIds.clear()


# / Modal/event Utils


def eventKeyIs(event, hotkey):
    return compareKmiWithKeybind(event, parseKeybindFromHotkeyString(hotkey))


def setModalTextInContext(context, headerText=None, statusText=None):
    try:
        context.area.header_text_set(text=headerText)
    except Exception as er:
        pass
    try:
        context.workspace.status_text_set(text=statusText)
    except Exception as er:
        pass


def addTimerForContext(context, time=0.3):
    return context.window_manager.event_timer_add(
        time, window=context.window)


def removeTimerFromContext(context, timer):
    return context.window_manager.event_timer_remove(
        timer) and None if timer else None


# / Area Utils


def getSpaceUnderMouseFromContextEvent(context, event):
    for area in context.screen.areas:
        if isAreaUnderMousePointer(area, event.mouse_prev_x, event.mouse_prev_y):
            return area.spaces[0]
    return None


def isAreaUnderMousePointer(area, x, y):
    inX = x >= area.x and x <= area.x + area.width
    inY = y >= area.y and y <= area.y + area.height
    return inX and inY


# / Tool Utils


def isToolSelect(tool):
    return tool in [
        'builtin.select', 'builtin.select_box', 'builtin.select_circle', 'builtin.select_lasso']


def setActiveToolInContext(tool=""):
    if tool:
        toolName = "builtin." + tool
        bpy.ops.wm.tool_set_by_id(name=toolName)


# Brush


def getActiveBrushTextureInContext(context):
    try:
        if context.mode == 'SCULPT':
            return context.tool_settings.sculpt.brush.texture
        elif context.mode == 'PAINT_VERTEX':
            return context.tool_settings.vertex_paint.brush.texture
        elif context.mode == 'PAINT_WEIGHT':
            return context.tool_settings.weight_paint.brush.texture
        elif context.mode == 'PAINT_TEXTURE':
            return context.tool_settings.image_paint.brush.texture
    except Exception as er:
        return None


def setActiveBrushTextureImageInContext(context, image):
    try:
        if context.mode == 'SCULPT':
            context.tool_settings.sculpt.brush.texture.image = image
        elif context.mode == 'PAINT_VERTEX':
            context.tool_settings.vertex_paint.brush.texture.image = image
        elif context.mode == 'PAINT_WEIGHT':
            context.tool_settings.weight_paint.brush.texture.image = image
        elif context.mode == 'PAINT_TEXTURE':
            context.tool_settings.image_paint.brush.texture.image = image
    except Exception as er:
        pass


def getActiveBrushMaskTextureInContext(context):
    try:
        if context.mode == 'PAINT_TEXTURE':
            return context.tool_settings.image_paint.brush.mask_texture
    except Exception as er:
        return None


def setActiveBrushMaskTextureImageInContext(context, image):
    try:
        if context.mode == 'PAINT_TEXTURE':
            context.tool_settings.image_paint.brush.mask_texture.image = image
    except Exception as er:
        pass


# / Object Utils


def findBpyObjectByName(name, col=None):
    col = bpy.data.objects if col == None else col
    for obj in col:
        if obj.name == name:
            return obj
    return None


def selectObjectByName(name):
    obj = findBpyObjectByName(name)
    if obj:
        obj.select_set(True)


def getObjectCollection(obj):
    try:
        col = obj.users_collection[0]
    except Exception as er:
        col = None
    return col


def moveObjectToCollection(obj, newCol):
    col = getObjectCollection(obj)
    if obj and col:
        col.objects.unlink(obj)  # unlink old
    if obj and newCol:
        newCol.objects.link(obj)  # link new


# Material/color


def appendNewActMatToObject(obj, diffuseColor=(1.0, 1.0, 1.0, 1.0), matSlot=None):
    newMat = bpy.data.materials.new("Material")
    newMat.diffuse_color = diffuseColor
    if not matSlot:
        obj.data.materials.append(newMat)
    else:
        matSlot.material = newMat
    obj.active_material = newMat
    return newMat


def ensureActMatForActObjectInContext(context):
    actObj = context.active_object
    actObjActMat = actObj.active_material
    actObjActMatIdx = actObj.active_material_index
    noMatSlots = not actObj.material_slots or not len(
        actObj.material_slots)

    if not actObjActMat:
        if noMatSlots:
            actObjActMat = appendNewActMatToObject(actObj)
        elif not actObj.material_slots[actObjActMatIdx].material:
            actObjActMat = appendNewActMatToObject(
                actObj, matSlot=actObj.material_slots[actObjActMatIdx])


def getObjectUsersOfMat(mat, col):
    # From https://blender.stackexchange.com/a/19021/179841
    users = []
    for obj in col:
        if isinstance(obj.data, bpy.types.Mesh) and mat.name in obj.data.materials:
            users.append(obj)
    return users


def appendNewColorAttrForObject(obj, name):
    if obj and obj.data:
        obj.data.color_attributes.new(
            name=name, type='BYTE_COLOR', domain='CORNER')


# Transformation


def applyObjectTransformsWithContext(context, obj, transforms=['location', 'rotation', 'scale']):
    with context.temp_override(selected_editable_objects=[obj]):
        bpy.ops.object.transform_apply(
            location='location' in transforms, rotation='rotation' in transforms, scale='scale' in transforms)


# Active/selected


def getOutlinerActivatedObjectsFromContext(context):
    selected_ids = context.selected_ids
    return [sel for sel in selected_ids if sel.rna_type.name != 'Collection']


def selectUnhideAllInGroup(group):
    for obj in bpy.data.objects:
        if obj.users_collection == group:
            obj.hide_set(False)
            obj.select_set(True)


def getObjectModeFromContext(context):
    contextMode = context.mode
    if contextMode == 'OBJECT' or 'PENCIL' in contextMode:
        return 'OBJECT'
    elif contextMode.startswith("EDIT"):
        return 'EDIT'
    elif contextMode.startswith("SCULPT"):
        return 'SCULPT'
    elif contextMode.startswith("PAINT"):
        modeParts = contextMode.split('_')
        return modeParts[1] + '_' + modeParts[0]
    else:
        return 'OBJECT'


def setActiveObjectInContext(context, obj, mode="", delPrev=False):
    if not obj:
        return

    if not delPrev:
        context.active_object.select_set(False)
    else:
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.delete()

    obj.select_set(True)
    context.view_layer.objects.active = obj

    if mode:
        bpy.ops.object.mode_set(mode=mode)


def deselectAllExceptActiveInContext(context):
    for obj in context.selected_objects:
        if obj != context.active_object:
            obj.select_set(False)


def rayCastInContextEvent(context, event):
    credits = [
        "https://devtalk.blender.org/t/pick-material-under-mouse-cursor/6978/7",
        "https://blender.stackexchange.com/a/192812/179841"
    ]

    # Get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y
    depsgraph = context.evaluated_depsgraph_get()

    # Get the ray from the viewport and mouse
    view_vector = bpy_extras.view3d_utils.region_2d_to_vector_3d(
        region, rv3d, coord)
    ray_origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(
        region, rv3d, coord)

    wasCasted, location, normal, castedPolyIdx, castedObj, matrix = scene.ray_cast(
        depsgraph, ray_origin, view_vector)

    return wasCasted, location, normal, castedPolyIdx, castedObj, matrix


def selectObjectUnderMouseFromContextEvent(context, event):
    hit, location, normal, polygonIdx, obj, matrix = rayCastInContextEvent(
        context, event)

    if not hit:
        return False

    if not obj.visible_get():
        return False

    obj.select_set(True)

    return True


def selectFaceUnderMouseFromContextEvent(context, event, onlyVisible=True):
    hit, location, normal, polygonIdx, obj, matrix = rayCastInContextEvent(
        context, event)

    if not hit:
        return False

    if onlyVisible and obj.data.polygons[polygonIdx].hide:
        return False

    bpy.ops.object.mode_set(
        mode='OBJECT')  # polygon.select works only in object mode \
    obj.data.polygons.active = polygonIdx
    obj.data.polygons[polygonIdx].select = True
    obj.data.update()

    return True


# Mesh


def getSelectedVerticesOfObject(obj):
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    return list(filter(lambda v: v.select, obj.data.vertices))


def getMeshFromObject(obj):
    return bmesh.from_edit_mesh(obj.data)


def getSelectedFacesOfMesh(mesh):
    selectedFaces = []
    for face in mesh.faces:
        if face.select:
            selectedFaces.append(face)
    return selectedFaces


def areAllFacesSelectedInObject(obj):
    mesh = getMeshFromObject(obj)
    selectedFaces = getSelectedFacesOfMesh(mesh)
    return len(selectedFaces) == len(mesh.faces)


# Curve


def createCurveAndEditInContext(context, name="Curve", inFront=False, tool='draw'):
    curveData = bpy.data.curves.new('Curve', type='CURVE')
    curveData.dimensions = '3D'
    curve = bpy.data.objects.new(name, curveData)
    curve.show_in_front = True if inFront else False
    context.collection.objects.link(curve)

    setActiveObjectInContext(context, curve, mode='EDIT')
    setActiveToolInContext(tool=tool)

    return curve


def getCurvePointsAll(curve):
    points = []
    for spline in curve.data.splines:
        for point in spline.bezier_points:
            points.append(point)
    return points


def getCurveActivePoint(curve, returnIfActiveLeftOrRight=False):
    for spline in curve.data.splines:
        for point in spline.bezier_points:
            if point.select_control_point:
                return point
            elif returnIfActiveLeftOrRight and (point.select_left_handle or point.select_right_handle):
                return point
    return None


def selectWholeBezierPoint(point, select=True):
    if point:
        point.select_control_point = select
        point.select_left_handle = select
        point.select_right_handle = select


def setCurveCyclic(curve, doCycle):
    for s in curve.data.splines:
        s.use_cyclic_u = doCycle


def isCurveMainSplineClosed(curve):
    return curve.data.splines[0].use_cyclic_u


# Modifiers


def moveObjectModifierAtTheEnd(obj, mod):
    modIdx = -1
    if obj.modifiers:
        for i, m in enumerate(obj.modifiers):
            if m.name == mod.name:
                modIdx = i
    if modIdx == -1 or modIdx == len(obj.modifiers) - 1:
        return
    obj.modifiers.move(modIdx, len(obj.modifiers) - 1)


# / UV Utils


def createUvTransformer(angle, origin=(0, 0), offset=(0, 0), scale=(1, 1)):
    cos_theta, sin_theta = math.cos(angle), math.sin(angle)
    x0, y0 = origin
    offset_x, offset_y = offset
    scale_x, scale_y = scale

    def xform(point):
        x = (point[0] - x0) * scale_x + offset_x
        y = (point[1] - y0) * scale_y + offset_y
        return (x * cos_theta - y * sin_theta + x0,
                x * sin_theta + y * cos_theta + y0)
    return xform
