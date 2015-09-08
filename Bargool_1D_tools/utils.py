__author__ = 'Alexey.Nakoryakov'

import bpy
from bpy.props import StringProperty
import collections


def flatten(*args):
    """ Flattens list of lists to flat list """
    for item in args:
        if isinstance(item, collections.Iterable) and not isinstance(item, (str, bytes)):
            for sub in flatten(item):
                yield sub
        else:
            yield item


def check_equality(lst1, lst2, tolerance):
    """ Checks equality of lists of numbers """
    for i1, i2 in zip(lst1, lst2):
        if abs(i1 - i2) > tolerance:
            return False
    return True


def drop_selection(scene):
    for o in scene.objects:
        o.select = False


def slugify(s):
    return s.lower().replace(' ', '_')


class OpenFileHelper(object):
    filepath = StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        subtype='FILE_PATH',
        )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class BatchOperatorMixin(object):
    """
    Base class for batch processing objects
    Inheritors must define:
        filter_object method to define what objects to process
        process_object method to define what to do with each object
    This mixin is for use in batch_operator_factory, because most of operators
    just filter some objects and make simple things with them
    """
    bl_options = {'REGISTER', 'UNDO'}

    use_selected_objects = True
    context = None

    def execute(self, context):
        """
        Template method pattern
        Must override filter_object and process_object
        """
        self.context = context
        # Select and filter objects
        if self.use_selected_objects:
            objects = context.selected_objects
        else:
            drop_selection(context.scene)
            objects = context.scene.objects
        self.pre_process_objects()
        work_objects = [obj for obj in objects if self.filter_object(obj)]
        # Cache old active object. At the end we will return activeness
        old_active = bpy.context.scene.objects.active
        for obj in work_objects:
            # As I understood, objects for bpy.ops operators must be
            # active in most cases
            bpy.context.scene.objects.active = obj
            # Fight!
            self.process_object(obj)
        bpy.context.scene.objects.active = old_active
        return {'FINISHED'}

    def filter_object(self, obj):
        return True

    def process_object(self, obj):
        pass

    def pre_process_objects(self):
        pass


def batch_operator_factory(operator_name, name, filter_func=None, process_func=None, use_selected_objects=True):
    bl_idname = '.'.join(('object', slugify(name)))
    d = {'bl_label': name,
         'bl_idname': bl_idname,
         'use_selected_objects': use_selected_objects, }
    if filter_func:
        d['filter_object'] = filter_func
    if process_func:
        d['process_object'] = process_func
    return type(operator_name, (BatchOperatorMixin, bpy.types.Operator), d)