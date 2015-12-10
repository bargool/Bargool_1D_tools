# -*- coding: utf-8 -*-

import bpy
import bmesh
from .geometry_utils import create_slope_plane, Point


class AlignToSlopeOperator(bpy.types.Operator):
    bl_idname = 'object.align_to_slope'
    bl_label = 'Pick To Slope'
    bl_options = {'REGISTER', 'UNDO'}

    class OPERATOR_TYPE_ENUM:
        do_remember = 'DO_REMEMBER'
        do_execute = 'DO_EXECUTE'

    operator_type = bpy.props.EnumProperty(items=((OPERATOR_TYPE_ENUM.do_execute,) * 3,
                                                  (OPERATOR_TYPE_ENUM.do_remember,) * 3),
                                           options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]

        if self.operator_type == self.OPERATOR_TYPE_ENUM.do_remember:
            if len(selected_verts) != 2:
                raise AssertionError
            if not selected_verts:
                self.report({'ERROR'}, 'Must select vertices previously')
                return {'CANCELLED'}
            selected_points = [Point(vert.co.x, vert.co.y, vert.co.z) for vert in selected_verts]
            context.scene.test_props.slope_plane = create_slope_plane(*selected_points)
        else:
            slope_plane = context.scene.test_props.slope_plane
            if not slope_plane:
                self.report({'ERROR'}, 'Must remember vertices previously')
                return {'CANCELLED'}
            inbound_only = context.scene.batch_operator_settings.geometry_inbound_only
            skipped_count = 0
            for v in selected_verts:
                z = slope_plane.get_z(v.co.x, v.co.y)
                if inbound_only:
                    if slope_plane.selected_z_lower <= z <= slope_plane.selected_z_upper:
                        v.co.z = z
                    else:
                        skipped_count += 1
                else:
                    v.co.z = z
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')
            if skipped_count:
                self.report({'INFO'}, 'Skipped {} vertices'.format(skipped_count))
        return {'FINISHED'}


def create_panel(col, scene):
    col.operator(AlignToSlopeOperator.bl_idname,
                 text='Store slope').operator_type = AlignToSlopeOperator.OPERATOR_TYPE_ENUM.do_remember
    col.operator(AlignToSlopeOperator.bl_idname,
                 text='Align to slope').operator_type = AlignToSlopeOperator.OPERATOR_TYPE_ENUM.do_execute
    col.prop(scene.batch_operator_settings,
             'geometry_inbound_only')
