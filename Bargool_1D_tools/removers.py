# -*- coding: utf-8 -*-
import abc
import bpy
from . import utils

__author__ = 'Aleksey Nakoryakov'


class BatchRemoverMixin(utils.BatchOperatorMixin):
    """
    Base mixin for batch processing objects
    Inheritors must override:
        filter_object method to define what objects to process
        process_object method to define what to do with each object
    """
    class OPERATOR_TYPE_ENUM:
        do_select = 'DO_SELECT'
        do_remove = 'DO_REMOVE'

    operator_type = bpy.props.EnumProperty(items=((OPERATOR_TYPE_ENUM.do_remove, )*3,
                                                  (OPERATOR_TYPE_ENUM.do_select, )*3),
                                           options={'HIDDEN'})

    @classmethod
    def poll(cls, context):
        return (context.selected_objects or
                context.scene.batch_operator_settings.work_without_selection)

    def get_use_selected_objects(self):
        return not self.context.scene.batch_operator_settings.work_without_selection

    def pre_filter_objects(self):
        self.count = 0

    def process_object(self, obj):
        self.count += 1
        if self.operator_type == self.OPERATOR_TYPE_ENUM.do_select:
            obj.select = True
        else:
            self.do_remove(obj)

    def post_process_objects(self):
        message = '{} {} properties'.format(
            'Removed' if self.operator_type == self.OPERATOR_TYPE_ENUM.do_remove else 'Selected',
            self.count
        )
        self.report({'INFO'}, message)

    # @abc.abstractmethod
    def do_remove(self, obj):
        raise NotImplementedError


class BatchUVMapsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.uvmaps_eraser'
    bl_label = 'UV Maps Batch Remove'
    bl_description = 'Removes UV Maps from selected or all objects in scene'
    dropdown_name = 'UV Maps'

    # operator_type = bpy.props.EnumProperty(items=(BatchRemoverMixin.OPERATOR_TYPE_ENUM.do_remove,
    #                                               BatchRemoverMixin.OPERATOR_TYPE_ENUM.do_select),
    #                                        options={'HIDDEN'})

    def filter_object(self, obj):
        """ We need to remove uv_textures. So we need objects with them """
        # I didn't see blender yet, so I don't know what objects have textures
        # so just find them
        return hasattr(obj.data, 'uv_textures') and obj.data.uv_textures

    def do_remove(self, obj):
        count = 0
        while obj.data.uv_textures:
            bpy.ops.mesh.uv_texture_remove()
            count += 1
        return count


class BatchVertexGroupEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.vertex_groups_eraser'
    bl_label = 'Vertex Groups Batch Remove'
    bl_description = 'Removes Vertex Groups from '\
                     'selected or all objects in scene'
    dropdown_name = 'Vertex Groups'

    def filter_object(self, obj):
        has_groups = (hasattr(obj, 'vertex_groups') and
                      obj.vertex_groups)
        return has_groups

    def do_remove(self, obj):
        bpy.ops.object.vertex_group_remove(all=True)
        # We try to count removed items, so return something
        return 1


class BatchShapeKeysEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.shape_keys_eraser'
    bl_label = 'Shape Keys Batch Remove'
    bl_description = 'Removes Shape Keys from selected or all objects in scene'
    dropdown_name = 'Shape Keys'

    def filter_object(self, obj):
        has_keys = hasattr(obj.data, 'shape_keys') and obj.data.shape_keys
        return True if has_keys else False

    def do_remove(self, obj):
        bpy.ops.object.shape_key_remove(all=True)
        # We try to count removed items, so return something
        return 1


class BatchVertexColorsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.vertex_colors_eraser'
    bl_label = 'Vertex Colors Batch Remove'
    bl_description = 'Removes VCols from selected or all objects in scene'
    dropdown_name = 'Vertex Colors'

    def filter_object(self, obj):
        has_colors = (hasattr(obj.data, 'vertex_colors') and
                      obj.data.vertex_colors)
        return True if has_colors else False

    def do_remove(self, obj):
        count = 0
        while obj.data.vertex_colors:
            for color in obj.data.vertex_colors:
                # Have to make vcolor active to remove it
                color.active = True
                bpy.ops.mesh.vertex_color_remove()
                # count is wrong because there is no guarantee that
                # vertex_color_remove tries to our active color
                count += 1
        return count


class BatchMaterialEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.materials_eraser'
    bl_label = 'Materials Batch Remove'
    bl_description = 'Removes Materials from selected or all objects in scene'
    dropdown_name = 'Materials'

    def filter_object(self, obj):
        has_materials = hasattr(obj.data, 'materials') and obj.data.materials
        return True if has_materials else False

    def do_remove(self, obj):
        count = 0
        while obj.data.materials:
            bpy.ops.object.material_slot_remove()
            count += 1
        return count


class BatchGPencilEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.gpencil_eraser'
    bl_label = 'GPencil Batch Remove'
    bl_description = 'Removes GPencils from selected or all objects in scene'
    dropdown_name = 'Grease Pencil'

    def filter_object(self, obj):
        has_materials = hasattr(obj, 'grease_pencil') and obj.grease_pencil
        return True if has_materials else False

    def do_remove(self, obj):
        count = 0
        while obj.grease_pencil:
            bpy.ops.gpencil.data_unlink()
            count += 1
        return count


class AllModifiersEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.all_modifiers_eraser'
    bl_label = 'All Modifiers Batch Remove'
    bl_description = 'Removes All Modifiers from '\
                     'selected or all objects in scene'
    dropdown_name = 'All Modifiers'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and obj.modifiers
        return True if has_modifiers else False

    def do_remove(self, obj):
        count = 0
        for modifier in obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class AllSubsurfsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.all_subsurfs_eraser'
    bl_label = 'All Subsurfs Batch Remove'
    bl_description = 'Removes All Subsurfs from selected '\
                     'or all objects in scene'
    dropdown_name = 'All Subsurfs'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers')
        if has_modifiers:
            has_subsurfs = len([m for m in obj.modifiers if m.type == 'SUBSURF']) > 0
            has_modifiers = has_modifiers and has_subsurfs
        return True if has_modifiers else False

    def do_remove(self, obj):
        count = 0
        subsurfs = [m for m in obj.modifiers if m.type == 'SUBSURF']
        for modifier in subsurfs:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class ZeroSubsurfsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.zero_subsurfs_eraser'
    bl_label = 'Zero Subsurfs Batch Remove'
    bl_description = 'Removes Subsurfs with view 0 from '\
                     'selected or all objects in scene'
    dropdown_name = 'Zero Subsurfs'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers')
        if has_modifiers:
            has_subsurfs = len([m for m in obj.modifiers
                                if m.type == 'SUBSURF' and m.levels == 0]) > 0
            has_modifiers = has_modifiers and has_subsurfs
        return True if has_modifiers else False

    def do_remove(self, obj):
        count = 0
        subsurfs = [m for m in obj.modifiers
                    if m.type == 'SUBSURF' and m.levels == 0]
        for modifier in subsurfs:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class EdgeSplitRemoverOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.edge_split_remover'
    bl_label = 'Edge Split Batch Remove/Select'
    bl_description = 'Removes/selects Edge Splits from selected or all objects in scene'
    dropdown_name = 'Edge Split'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers')
        return has_modifiers and any([m for m in obj.modifiers if m.type == 'EDGE_SPLIT'])

    def do_remove(self, obj):
        count = 0
        edge_splits = [m for m in obj.modifiers if m.type == 'EDGE_SPLIT']
        for modifier in edge_splits:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class MirrorMDFRemoverOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.mirror_mdf_remover'
    bl_label = 'Mirror modifier Batch Remove/Select'
    bl_description = 'Removes/selects Mirror modifier from selected or all objects in scene'
    dropdown_name = 'Mirror'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers')
        return has_modifiers and any([m for m in obj.modifiers if m.type == "MIRROR"])

    def do_remove(self, obj):
        count = 0
        mirrors = [m for m in obj.modifiers if m.type == 'MIRROR']
        for modifier in mirrors:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1


def create_panel_rems(col, scene):
    col.operator(scene.batch_operator_settings.removers_dropdown,
                 text='Remove').operator_type = BatchRemoverMixin.OPERATOR_TYPE_ENUM.do_remove
    col.operator(scene.batch_operator_settings.removers_dropdown,
                 text='Select').operator_type = BatchRemoverMixin.OPERATOR_TYPE_ENUM.do_select
    col.prop(scene.batch_operator_settings, 'removers_dropdown',
             text='Action')
    col.prop(scene.batch_operator_settings, 'work_without_selection')
