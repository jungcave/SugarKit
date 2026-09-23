DIV = 100


# ! TODO: add condition that object must be unwrapped (has at least one uv)
# TODO: 3.2.x Complete resetTransformation()
class PaintMaskUvTransformProps(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(name="Angle", default=0,  min=-180, max=180,
                                   update=lambda self, context: self.updateProp(
                                       self, context, 'angle'))
    offset_x: bpy.props.FloatProperty(name="Offset X", default=0, min=-DIV, max=DIV,
                                      update=lambda self, context: self.updateProp(
                                          self, context, 'offset_x'))
    offset_y: bpy.props.FloatProperty(name="Offset Y", default=0, min=-DIV, max=DIV,
                                      update=lambda self, context: self.updateProp(
                                          self, context, 'offset_y'))
    scale_x: bpy.props.IntProperty(name="Scale X", default=DIV, min=1, max=2*DIV,
                                   update=lambda self, context: self.updateProp(
                                       self, context, 'scale_x'))
    scale_y: bpy.props.IntProperty(name="Scale Y", default=DIV, min=1, max=2*DIV,
                                   update=lambda self, context: self.updateProp(
                                       self, context, 'scale_y'))
    scale_both: bpy.props.BoolProperty(default=True,
                                       update=lambda self, context: self.updateScaleBoth(
                                           self, context))
    scale_xy: bpy.props.IntProperty(name="Scale", default=DIV, min=1, max=2*DIV,
                                    update=lambda self, context: self.updateScale(
                                        self, context))
    do_transformation_reset: bpy.props.BoolProperty(name='Reset All',
                                                    update=lambda self, context: self.resetTransformation(self, context))

    prev_uv_rotation_angle: bpy.props.FloatProperty(name='', default=0)
    prev_uv_translation_x: bpy.props.FloatProperty(name='', default=0)
    prev_uv_translation_y: bpy.props.FloatProperty(name='', default=0)
    prev_uv_scale_x: bpy.props.IntProperty(name='', default=DIV)
    prev_uv_scale_y: bpy.props.IntProperty(name='', default=DIV)

    # Get prop: context.active_object.xx_paint_mask_uv_transform
    # Set prop: bpy.types.Object.xx_paint_mask_uv_transform

    @classmethod
    def updateProp(cls, self, context, propname, propvalue=None):
        global glob

        try:
            actObjData = context.active_object.data
        except Exception as er:
            actObjData = None
        try:
            stencilUv = context.active_object.data.uv_layer_stencil
        except Exception as er:
            stencilUv = None

        if not actObjData or not stencilUv:
            return

        origin_x = 0.5 + self.prev_uv_translation_x/DIV
        origin_y = 0.5 + self.prev_uv_translation_y/DIV
        scale_x = self.scale_x if not propvalue else propvalue
        scale_y = self.scale_y if not propvalue else propvalue
        SCALE_MULTIPLIER = 4  # the more the scale multiplier, the more possible scale range (min = 1) \
        INCREASE_PROPORTION = 1 + SCALE_MULTIPLIER/DIV
        DECREASE_PROPORTION = 1 - SCALE_MULTIPLIER/(DIV + 1)

        # Angle
        if propname == 'angle':
            angle = self.angle - self.prev_uv_rotation_angle
            rotateUv = createUvTransformer(
                math.radians(angle), (origin_x, origin_y))

            for v in actObjData.loops:
                stencilUv.data[v.index].uv = rotateUv(
                    stencilUv.data[v.index].uv)

            self.prev_uv_rotation_angle = self.angle
        # Offset
        elif propname == 'offset_x':
            offsetX = -1*(self.offset_x - self.prev_uv_translation_x)/DIV
            translateUv = createUvTransformer(
                0, (0.5, 0.5), (offsetX, 0))

            for v in actObjData.loops:
                stencilUv.data[v.index].uv = translateUv(
                    stencilUv.data[v.index].uv)

            self.prev_uv_translation_x = self.offset_x
        elif propname == 'offset_y':
            offsetY = -1*(self.offset_y - self.prev_uv_translation_y)/DIV
            translateUv = createUvTransformer(
                0, (0.5, 0.5), (0, offsetY))

            for v in actObjData.loops:
                stencilUv.data[v.index].uv = translateUv(
                    stencilUv.data[v.index].uv)

            self.prev_uv_translation_y = self.offset_y
        # Scale
        elif propname == 'scale_x':
            diffX = scale_x - self.prev_uv_scale_x
            scaleX = DECREASE_PROPORTION if diffX > 0 else INCREASE_PROPORTION
            scaleUv = createUvTransformer(
                0, (origin_x, origin_y), (0, 0), (scaleX, 1))

            for _ in range(abs(diffX)):
                for v in actObjData.loops:
                    stencilUv.data[v.index].uv = scaleUv(
                        stencilUv.data[v.index].uv)

            self.prev_uv_scale_x = scale_x
        elif propname == 'scale_y':
            diffY = scale_y - self.prev_uv_scale_y
            scaleY = DECREASE_PROPORTION if diffY > 0 else INCREASE_PROPORTION
            scaleUv = createUvTransformer(
                0, (origin_x, origin_y), (0, 0), (1, scaleY))

            for _ in range(abs(diffY)):
                for v in actObjData.loops:
                    stencilUv.data[v.index].uv = scaleUv(
                        stencilUv.data[v.index].uv)

            self.prev_uv_scale_y = scale_y

    @classmethod
    def updateScaleBoth(cls, self, context):
        if not self.scale_both:
            self.scale_x = self.scale_xy
            self.scale_y = self.scale_xy
        else:
            self.scale_xy = DIV

    @classmethod
    def updateScale(cls, self, context):
        self.updateProp(self, context, 'scale_x', self.scale_xy)
        self.updateProp(self, context, 'scale_y', self.scale_xy)

    @classmethod
    def resetTransformation(cls, self, context):
        C()


class PaintMaskUvTransformPanelOperator(bpy.types.Operator):
    bl_label = "Paint Mask Transform Form Panel"
    bl_idname = "paint.xx_paint_mask_uv_transform_panel"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            hasStencilImage = context.tool_settings.image_paint.stencil_image
        except Exception as er:
            hasStencilImage = None

        if not hasStencilImage:
            self.report({'INFO'}, "Mask stencil image hasn't been set!")
            return {'FINISHED'}

        bpy.ops.wm.call_panel(
            name=PaintMaskUvTransformPanel.bl_idname)
        return {'FINISHED'}


class PaintMaskUvTransformPanel(bpy.types.Panel):
    bl_space_type = 'TOPBAR'  # requered panel dummy
    bl_region_type = 'HEADER'  # requered panel dummy
    bl_label = "Stencil Mask Transform"
    bl_idname = "sk_paint_mask_uv_transform_panel"
    bl_ui_units_x = 20  # width

    def draw(self, context):
        layout = self.layout
        props = context.active_object.xx_paint_mask_uv_transform

        layout.prop(props, "angle", slider=True)
        layout.prop(props, "offset_x", slider=True)
        layout.prop(props, "offset_y", slider=True)

        split = layout.split(factor=0.9)
        col1 = split.column()
        scaleRow = col1.row(align=True)
        col2 = split.column()

        if not props.scale_both:
            scaleRow.prop(props, "scale_x", slider=True)
            scaleRow.prop(props, "scale_y", slider=True)
            col2.prop(props, "scale_both", toggle=True,
                      icon="ORIENTATION_VIEW", text="")
        else:
            scaleRow.prop(props, "scale_xy", slider=True)
            col2.prop(props, "scale_both", toggle=True,
                      icon="ORIENTATION_VIEW", text="")

        # layout.prop(props, "do_transformation_reset")

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