import collections

import bpy
from bpy_extras.io_utils import ExportHelper

from .utils import check_equality, OpenFileHelper, BatchOperatorMixin, draw_operator

__author__ = 'Aleksey Nakoryakov'


def is_multiuser(obj):
    """ Test for instances """
    return hasattr(obj.data, 'users') and obj.data.users > 1


def find_instances(obj, context):
    """ Finds instances of object obj """
    if not hasattr(obj.data, 'name'):
        return
    mesh_name = obj.data.name
    for o in filter_named_data(context.scene.objects):
        if o.data.name == mesh_name:
            yield o


def create_instance(obj, scene):
    """ Creates instance of obj """
    duplicated = obj.copy()
    scene.objects.link(duplicated)
    return duplicated


def filter_named_data(items):
    return [o for o in items if hasattr(o.data, 'name')]


class BlockInstance(object):
    """ Class for operating with instances read from txt file """
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], collections.Iterable):
            s = args[0]
            s = s.strip()
            s = s.replace('(', '')
            s = s.replace(')', '')
            args = s.split()
        elif len(args) == 1 and isinstance(args[0], bpy.types.Object):
            o = args[0]
            self.obname = o.name
            self.name = o.data.name
            self.coords = list(o.location)
            self.scale = list(o.scale)
            self.rotation = list(o.rotation_euler)
            return
        self.name = args[0]
        self.coords = list(map(float, args[1:4]))
        self.scale = list(map(float, args[4:7]))
        self.rotation = float(args[7])
        self.obname = None

    def __check_name(self, obj):
        if obj.data.name != self.name:
            raise AttributeError("Mesh name not equals")

    def modify_obj(self, obj):
        self.__check_name(obj)
        obj.location = self.coords
        obj.scale = self.scale
        obj.rotation_euler[2] = self.rotation

    def is_equals_to_obj(self, obj, tolerance):
        self.__check_name(obj)
        equality = (check_equality(obj.location.to_tuple(), self.coords, tolerance) and
                    check_equality(obj.scale.to_tuple(), self.scale, tolerance) and
                    check_equality([obj.rotation_euler[2], ], [self.rotation, ], tolerance))
        return equality

    def __str__(self):
        return ('("{obname}"\t"{name}"\t'
                '({coords[0]} {coords[1]} {coords[2]})\t'
                '({rot[0]} {rot[1]} {rot[2]})\t'
                '({sc[0]} {sc[1]} {sc[2]}))').format(obname=self.obname,
                                                     name=self.name,
                                                     coords=self.coords,
                                                     rot=self.rotation,
                                                     sc=self.scale)


def read_file(filepath):
    with open(filepath, 'r') as f:
        lst = [BlockInstance(l) for l in f if l.startswith('(')]
        d = {}
        for l in lst:
            if l.name not in d:
                d[l.name] = [l, ]
            else:
                d[l.name].append(l)
    return d


def write_file(filepath, items):
    with open(filepath, 'w') as f:
        f.writelines(["%s\n" % i for i in items])


class ImportTextAsInstancesOperator(OpenFileHelper, bpy.types.Operator):
    bl_idname = 'object.import_instances'
    bl_label = 'Place Instances'
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob = bpy.props.StringProperty(default="*.txt;",
                                           options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        instances_dict = read_file(self.filepath)
        objects = filter_named_data(scene.objects)
        for obj in objects:
            if obj.data.name in instances_dict:
                instances = instances_dict.pop(obj.data.name)
                for inst in instances:
                    duplicated = create_instance(obj, scene)
                    inst.modify_obj(duplicated)
        return {'FINISHED'}


class ExportInstancesAsTextOperator(ExportHelper, bpy.types.Operator):
    bl_idname = 'object.export_instances_as_text'
    bl_label = 'Export to text'
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".txt"

    def execute(self, context):
        objects = [BlockInstance(obj) for obj in filter_named_data(context.selected_objects)]
        write_file(self.filepath, objects)
        return {'FINISHED'}


class FindInstancesFromText(OpenFileHelper, bpy.types.Operator):
    bl_idname = 'object.find_instances'
    bl_label = 'Find Instances'
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob = bpy.props.StringProperty(default="*.txt;",
                                           options={'HIDDEN'})

    def execute(self, context):
        tolerance = context.scene.tool_settings.double_threshold
        scene = context.scene
        instances_dict = read_file(self.filepath)
        objects = filter_named_data(scene.objects)
        for obj in objects:
            if obj.data.name in instances_dict:
                d = instances_dict[obj.data.name]
                for index, item in enumerate(d):
                    if item.is_equals_to_obj(obj, tolerance):
                        obj.select = True
                        d.pop(index)
                        break
        return {'FINISHED'}


class DropInstancesOperator(bpy.types.Operator):
    bl_idname = 'object.drop_instances'
    bl_label = 'Drop Instances'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        acitive_object = context.active_object
        # object_layers = list(acitive_object.layers)
        matrices = [o.matrix_local for o in find_instances(acitive_object, context) if o.name != acitive_object.name]
        bpy.ops.mesh.separate()
        separated_object = scene.objects[0]
        # separated_object.layers = object_layers
        for m in matrices:
            duplicated = create_instance(separated_object, scene)
            duplicated.matrix_local = m

        return {'FINISHED'}


class InstancesToCursourOperator(bpy.types.Operator):
    bl_idname = 'object.instances_to_cursor'
    bl_label = 'Instances to cursor'
    bl_description = 'Creates instances of each selected multiuser into cursor position'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        cursor_location = scene.cursor_location
        selected_multiuser = [o for o in filter_named_data(context.selected_objects) if is_multiuser(o)]
        for o in context.selected_objects:
            o.select = False
        objects = {}
        # We need only one object of each seleceted mesh
        for o in selected_multiuser:
            if o.data.name not in objects:
                objects[o.data.name] = o

        for v in objects.values():
            duplicated = create_instance(v, scene)
            duplicated.location = cursor_location
            duplicated.select = True

        return {'FINISHED'}


class CombineOperator(BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.combine'
    bl_label = 'Combine objects'

    use_only_selected_objects = True

    def process_object(self, obj):
        obj.location = self.active_object.location
        obj.rotation_euler = self.active_object.rotation_euler
        obj.scale = self.active_object.scale


class SelectInstancesOperator(bpy.types.Operator):
    bl_idname = 'object.select_instances'
    # Double "II" just for quick "space" start of operator (space -> "ii", an there is operator)
    bl_label = 'Select IInstances'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        scene = context.scene
        selected_objects = filter_named_data(context.selected_objects)
        mesh_names = set([o.data.name for o in selected_objects])
        objects_to_select = [obj for obj in filter_named_data(scene.objects) if obj.data.name in mesh_names]
        for obj in objects_to_select:
            obj.select = True
        return {'FINISHED'}


class FilterInstancesOperator(BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.filter_instances'
    # Double "III" just for quick "space" start of operator (space -> "iii", an there is operator)
    bl_label = 'Filter IIInstances'
    bl_options = {'REGISTER', 'UNDO'}

    use_only_selected_objects = False
    mesh_names = {}

    def pre_filter_objects(self):
        self.objects = filter_named_data(self.objects)
        self.mesh_names = set([o.data.name for o in filter_named_data(self.selected_objects)])

    def filter_object(self, obj):
        return obj.data.name in self.mesh_names and is_multiuser(obj)

    def process_object(self, obj):
        obj.select = True


class DeselectInstancesOperator(BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.deselect_instances'
    bl_label = 'Deselect Instances'

    def filter_object(self, obj):
        return is_multiuser(obj)

    def process_object(self, obj):
        obj.select = False


def create_panel(col):
    operators = [
        ImportTextAsInstancesOperator.bl_idname,
        ExportInstancesAsTextOperator.bl_idname,
        FindInstancesFromText.bl_idname,
        (SelectInstancesOperator.bl_idname, 'Select Instances'),
        (FilterInstancesOperator.bl_idname, 'Filter Instances'),
        DeselectInstancesOperator.bl_idname,
        DropInstancesOperator.bl_idname,
        InstancesToCursourOperator.bl_idname,
        CombineOperator.bl_idname,
    ]
    for op in operators:
        draw_operator(col, op)
