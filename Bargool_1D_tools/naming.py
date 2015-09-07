__author__ = 'alexey.nakoryakov'

import bpy
from . import utils


class ObnameToMeshnameOperator(bpy.types.Operator):
    bl_idname = 'object.obname_to_meshname'
    bl_label = 'Obname To Meshname'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            obj.data.name = obj.name
        return {'FINISHED'}


class MeshnameToObnameOperator(bpy.types.Operator):
    bl_idname = 'object.meshname_to_obname'
    bl_label = 'Meshname To Obname'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
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


class AddAsObPrefixOperator(bpy.types.Operator):
    bl_idname = 'object.add_as_ob_prefix'
    bl_label = 'Add As ObPrefix'
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


class FindObNameOperator(bpy.types.Operator):
    bl_idname = 'object.find_ob_name'
    bl_label = 'Find ObName'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        search_string = context.active_object.name.lower()
        objects = [o for o in context.scene.objects if not o.hide and search_string in o.name.lower()]
        for o in objects:
            o.select = True
        return {'FINISHED'}


class FindMeshNameOperator(bpy.types.Operator):
    bl_idname = 'mesh.find_mesh_name'
    bl_label = 'Find MeshName'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        search_string = context.active_object.data.name.lower()
        objects = [o for o in context.scene.objects if not o.hide and search_string in o.data.name.lower()]
        for o in objects:
            o.select = True
        return {'FINISHED'}


def sel_obj(o, obj):
    obj.select = True

SelectObNameEqualsMeshNameOperator = utils.batch_operator_factory(
    "SelectObNameEqualsMeshNameOperator", "Select ObName equals MeshName", lambda o, x: x.name == x.data.name,
    sel_obj,
    use_selected_objects=False,
)


def register_this():
    bpy.utils.register_class(SelectObNameEqualsMeshNameOperator)
# class SelectObNameEqualsMeshNameOperator(utils.OperatorTemplateMixin, bpy.types.Operator):
#     # bl_idname = 'object.select_obname_eq_meshname'
#     bl_label = 'Select ObName == MeshName'
#     # bl_options = {'REGISTER', 'UNDO'}
#
#     def execute(self, context):
#         drop_selection(context.scene)
#         objects = [o for o in context.scene.objects if o.name == o.data.name]
#         for o in objects:
#             o.select = True
#         return {'FINISHED'}