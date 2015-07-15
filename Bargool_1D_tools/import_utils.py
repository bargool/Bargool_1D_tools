# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import collections
import bpy
from . import utils


def is_multiuser(obj):
    return obj.data.users > 1


class ImportCleanupOperator(bpy.types.Operator):
    """ Class by Paul Kotelevets, and my little edits """
    bl_idname = 'mesh.import_cleanup'
    bl_label = 'Obj Import Cleanup'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        objects = [o for o in context.selected_objects if
                   o.type == 'MESH' and o.is_visible(scene)]
        for ob in objects:
            ob.select = True
            context.scene.objects.active = ob
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)
            bpy.ops.mesh.tris_convert_to_quads(limit=0.698132, uvs=False,
                                               vcols=False, sharp=False,
                                               materials=False)
            # Tada!!
            settings = context.scene.batch_operator_settings
            do_recalculate_normals = settings.import_cleanup_recalculate_normals
            if do_recalculate_normals:
                bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
            do_import_cleanup_apply_rotations = settings.import_cleanup_apply_rotations
            if do_import_cleanup_apply_rotations and not is_multiuser(ob):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        return {'FINISHED'}


def flatten(*args):
    for item in args:
        if isinstance(item, collections.Iterable) and not isinstance(item, (str, bytes)):
            for sub in flatten(item):
                yield sub
        else:
            yield item


def check_equality(lst1, lst2, tolerance):
    for i1, i2 in zip(lst1, lst2):
        if abs(i1 - i2) > tolerance:
            return False
    return True


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


class ImportTextAsInstancesOperator(utils.OpenFileHelper, bpy.types.Operator):
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
                    duplicated = obj.copy()
                    scene.objects.link(duplicated)
                    inst.modify_obj(duplicated)
        return {'FINISHED'}


class FindInstancesFromText(utils.OpenFileHelper, bpy.types.Operator):
    bl_idname = 'object.find_instances'
    bl_label = 'Find Snstances'
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