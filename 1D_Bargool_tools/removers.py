# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy


class BatchRemoverMixin(object):
    """
    Base mixin for batch processing objects
    Inheritors must override:
        filter_object method to define what objects to process
        process_object method to define what to do with each object
    """
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.selected_objects or
                context.scene.batch_operator_settings.work_without_selection)

    def execute(self, context):
        """
        Template method pattern
        Must override filter_object and process_object
        """
        # Count is just for debug stuff
        count = 0
        # Select and filter objects
        objects = context.selected_objects or bpy.data.objects
        work_objects = [obj for obj in objects if self.filter_object(obj)]
        # Cache old active object. At the end we will return activeness
        old_active = bpy.context.scene.objects.active
        for obj in work_objects:
            # As I understood, objects for bpy.ops operators must be
            # active in most cases
            bpy.context.scene.objects.active = obj
            # Fight!
            count += self.process_object(obj)
        bpy.context.scene.objects.active = old_active

        message = 'Removed {0} properties'.format(count)
        self.report({'INFO'}, message)

        return {'FINISHED'}

    def filter_object(self, obj):
        """
        Hey! You must redefine me!
        If you need obj - return True
        """
        raise NotImplementedError

    def process_object(self, obj):
        """
        Hey! You must redefine me!
        Here is most work will be
        """
        raise NotImplementedError


class BatchUVMapsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.uvmaps_eraser'
    bl_label = 'UV Maps Batch Remove'
    bl_description = 'Removes UV Maps from selected or all objects in scene'
    dropdown_name = 'UV Maps'

    def filter_object(self, obj):
        """ We need to remove uv_textures. So we need objects with them """
        # I didn't see blender yet, so I don't know what objects have textures
        # so just find them
        return hasattr(obj.data, 'uv_textures')

    def process_object(self, obj):
        count = 0
        while obj.data.uv_textures:
            bpy.ops.mesh.uv_texture_remove()
            count += 1
        return count


class BatchVertexGroupEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.vertex_groups_eraser'
    bl_label = 'Vertex Groups Batch Remove'
    bl_description = 'Removes Vertex Groups from ' \
                     'selected or all objects in scene'
    dropdown_name = 'Vertex Groups'

    def filter_object(self, obj):
        has_groups = (hasattr(obj, 'vertex_groups') and
                      len(obj.vertex_groups) > 0)
        return has_groups

    def process_object(self, obj):
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

    def process_object(self, obj):
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

    def process_object(self, obj):
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

    def process_object(self, obj):
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

    def process_object(self, obj):
        count = 0
        while obj.grease_pencil:
            bpy.ops.gpencil.data_unlink()
            count += 1
        return count


class AllModifiersEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.all_modifiers_eraser'
    bl_label = 'All Modifiers Batch Remove'
    bl_description = 'Removes All Modifiers from ' \
                     'selected or all objects in scene'
    dropdown_name = 'All Modifiers'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and len(obj.modifiers) > 0
        return True if has_modifiers else False

    def process_object(self, obj):
        count = 0
        for modifier in obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class AllSubsurfsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.all_subsurfs_eraser'
    bl_label = 'All Subsurfs Batch Remove'
    bl_description = 'Removes All Subsurfs from selected ' \
                     'or all objects in scene'
    dropdown_name = 'All Subsurfs'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and len(obj.modifiers) > 0
        return True if has_modifiers else False

    def process_object(self, obj):
        count = 0
        subsurfs = [m for m in obj.modifiers if m.type == 'SUBSURF']
        for modifier in subsurfs:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class ZeroSubsurfsEraserOperator(BatchRemoverMixin, bpy.types.Operator):
    bl_idname = 'object.zero_subsurfs_eraser'
    bl_label = 'Zero Subsurfs Batch Remove'
    bl_description = 'Removes Subsurfs with view 0 from ' \
                     'selected or all objects in scene'
    dropdown_name = 'Zero Subsurfs'

    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and len(obj.modifiers) > 0
        return True if has_modifiers else False

    def process_object(self, obj):
        count = 0
        subsurfs = [m for m in obj.modifiers
                    if m.type == 'SUBSURF' and m.levels == 0]
        for modifier in subsurfs:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count