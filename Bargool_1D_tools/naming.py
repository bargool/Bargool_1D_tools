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