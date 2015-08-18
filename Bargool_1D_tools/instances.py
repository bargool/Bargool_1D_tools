# -*- coding: utf-8 -*-

import bpy
from .utils import check_equality, OpenFileHelper

__author__ = 'alexey.nakoryakov'


def is_multiuser(obj):
    """ Test for instances """
    return obj.data.users > 1


def find_instances(obj, context):
    mesh_name = obj.data.name
    for o in context.scene.objects:
        if o.data.name == mesh_name:
            yield o


def create_instance(obj, scene):
    duplicated = obj.copy()
    scene.objects.link(duplicated)
    return duplicated


class BlockInstance(object):
    def __init__(self, *args):
        if len(args) == 1:
            s = args[0]
            s = s.strip()
            s = s.replace('(', '')
            s = s.replace(')', '')
            args = s.split()
        self.name = args[0]
        self.coords = list(map(float, args[1:4]))
        self.scale = list(map(float, args[4:7]))
        self.rotation = float(args[7])

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
        return '({} {} {} {})'.format(self.name, self.coords, self.scale, self.rotation)


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


class ImportTextAsInstancesOperator(OpenFileHelper, bpy.types.Operator):
    bl_idname = 'object.import_instances'
    bl_label = 'Place Instances'
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob = bpy.props.StringProperty(default="*.txt;",
                                           options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        instances_dict = read_file(self.filepath)
        objects = scene.objects[:]
        for obj in objects:
            if obj.data.name in instances_dict:
                instances = instances_dict.pop(obj.data.name)
                for inst in instances:
                    duplicated = create_instance(obj, scene)
                    inst.modify_obj(duplicated)
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
        objects = scene.objects
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
        matrices = [o.matrix_local for o in find_instances(acitive_object, context) if o.name != acitive_object.name]
        bpy.ops.mesh.separate()
        separated_object = scene.objects[0]
        for m in matrices:
            duplicated = create_instance(separated_object, scene)
            duplicated.matrix_local = m

        return {'FINISHED'}