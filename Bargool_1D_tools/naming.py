__author__ = 'alexey.nakoryakov'

import bpy
from . import utils


def remove_prefix(s):
    part = s.partition('_')
    return part[-1] or part[0]


def remove_suffix(s):
    part = s.rpartition('_')
    return part[0] or part[-1]


class ObnameToMeshnameOperator(utils.BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.obname_to_meshname'
    bl_label = 'Obname To Meshname'
    bl_description = 'Assigns object name to its meshname. Works with all selected objects'

    def process_object(self, obj):
        obj.data.name = obj.name


class MeshnameToObnameOperator(utils.BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.meshname_to_obname'
    bl_label = 'Meshname To Obname'
    bl_description = 'Assigns meshname to object name. Works with all selected objects'

    def process_object(self, obj):
        obj.name = obj.data.name


class ActiveNameMixin(utils.BatchOperatorMixin):
    """ Mixin to for with name of active object """
    def pre_process_objects(self):
        self.obname = self.context.active_object.name

    def filter_object(self, obj):
        return obj.name != self.obname


class DistributeObnameOperator(ActiveNameMixin, bpy.types.Operator):
    bl_idname = 'object.distribute_obname'
    bl_label = 'Distribute Obname'

    def process_object(self, obj):
        obj.name = self.obname

    def post_process_objects(self):
        self.context.active_object.name = self.obname


class AddAsObPrefixOperator(ActiveNameMixin, bpy.types.Operator):
    bl_idname = 'object.add_as_ob_prefix'
    bl_label = 'Add As ObPrefix'

    def process_object(self, obj):
        obj.name = '_'.join((self.obname, obj.name))


class RemoveObPrefixOperator(utils.BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.remove_obprefix'
    bl_label = 'Remove ObPrefix'

    def process_object(self, obj):
        obj.name = remove_prefix(obj.name)


class AddAsObSuffixOpperator(ActiveNameMixin, bpy.types.Operator):
    bl_idname = 'object.add_as_obsuffix'
    bl_label = 'Add As ObSuffix'

    def process_object(self, obj):
        obj.name = '_'.join((obj.name, self.obname))


class RemoveObSuffixOperator(utils.BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.remove_obsuffix'
    bl_label = 'Remove ObSuffix'

    def process_object(self, obj):
        obj.name = remove_suffix(obj.name)


class FindObNameOperator(utils.ObjectsSelectorMixin, bpy.types.Operator):
    bl_idname = 'object.find_ob_name'
    bl_label = 'Find ObName'
    use_selected_objects = False

    def pre_process_objects(self):
        self.search_string = self.context.active_object.name.lower()

    def filter_object(self, obj):
        return not obj.hide and self.search_string in obj.name.lower()


class FindMeshNameOperator(utils.ObjectsSelectorMixin, bpy.types.Operator):
    bl_idname = 'mesh.find_mesh_name'
    bl_label = 'Find MeshName'
    use_selected_objects = False

    def pre_process_objects(self):
        self.search_string = self.context.active_object.data.name.lower()

    def filter_object(self, obj):
        return not obj.hide and self.search_string in obj.data.name.lower()


class SelectObNameEqualsMeshNameOperator(utils.BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.select_obname_equals_meshname'
    bl_label = 'Select ObName == MeshName'

    use_selected_objects = False

    def filter_object(self, obj):
        return obj.name == obj.data.name

    def process_object(self, obj):
        obj.select = True


def create_panel(col):
    operators = [
        'object.obname_to_meshname',
        'object.meshname_to_obname',
        'object.distribute_obname',
        'object.add_as_ob_prefix',
        'object.remove_obprefix',
        'object.add_as_obsuffix',
        'object.remove_obsuffix'
        'object.find_ob_name',
        'mesh.find_mesh_name',
        'object.select_obname_equals_meshname',
        ]
    for op in operators:
        col.operator(op)