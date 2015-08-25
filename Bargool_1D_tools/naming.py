__author__ = 'alexey.nakoryakov'

import bpy


class ObnameToMeshnameOperator(bpy.types.Operator):
    bl_idname = 'object.obname_to_meshname'
    bl_label = 'Obname To Meshname'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        obj.data.name = obj.name
        return {'FINISHED'}


class MeshnameToObnameOperator(bpy.types.Operator):
    bl_idname = 'object.meshname_to_obname'
    bl_label = 'Meshname To Obname'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        obj.name = obj.data.name
        return {'FINISHED'}


class DistributeObnameOperator(bpy.types.Operator):
    bl_idname = 'object.distribute_obname'
    bl_label = 'Distribute Obname'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        name = obj.name
        selected_objects = [o for o in context.selected_objects if o.name != name]
        for o in selected_objects:
            o.name = name
        obj.name = name

        return {'FINISHED'}


class AddAsPrefixOperator(bpy.types.Operator):
    bl_idname = 'object.add_as_prefix'
    bl_label = 'Add As Prefix'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        name = obj.name
        selected_objects = [o for o in context.selected_objects if o.name != name]
        for o in selected_objects:
            o.name = '_'.join((name, o.name))
        return {'FINISHED'}


class RemovePrefixOperator(bpy.types.Operator):
    bl_idname = 'object.remove_prefix'
    bl_label = 'Remove Prefix'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for o in context.selected_objects:
            part = o.name.partition('_')
            o.name = part[-1] or part[0]

        return {'FINISHED'}