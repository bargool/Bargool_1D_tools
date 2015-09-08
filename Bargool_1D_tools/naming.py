__author__ = 'alexey.nakoryakov'

import bpy
from . import utils


def remove_prefix(s):
    part = s.partition('_')
    return part[-1] or part[0]


def remove_suffix(s):
    part = s.rpartition('_')
    return part[0] or part[-1]


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


class RemoveObPrefixOperator(bpy.types.Operator):
    bl_idname = 'object.remove_obprefix'
    bl_label = 'Remove ObPrefix'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for o in context.selected_objects:
            o.name = remove_prefix(o.name)

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


def select_object(o, obj):
    obj.select = True


def obname_to_meshname(o, obj):
    obj.data.name = obj.name


ObnameToMeshnameOperator = utils.batch_operator_factory(
    "ObnameToMeshnameOperator", "Obname To Meshname",
    process_func=obname_to_meshname,
    use_selected_objects=True
)

SelectObNameEqualsMeshNameOperator = utils.batch_operator_factory(
    "SelectObNameEqualsMeshNameOperator", "Select ObName equals MeshName", lambda o, x: x.name == x.data.name,
    select_object,
    use_selected_objects=False,
    )


def register_module():
    classes = [
        ObnameToMeshnameOperator,
        SelectObNameEqualsMeshNameOperator,
    ]
    for klass in classes:
        bpy.utils.register_class(klass)


def create_panel(col):
    operators = [
        ObnameToMeshnameOperator.bl_idname,
        'object.meshname_to_obname',
        'object.distribute_obname',
        'object.add_as_ob_prefix',
        'object.remove_obprefix',
        'object.find_ob_name',
        'mesh.find_mesh_name',
        SelectObNameEqualsMeshNameOperator.bl_idname,
        ]

    for op in operators:
        col.operator(op)