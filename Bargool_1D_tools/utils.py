__author__ = 'Alexey.Nakoryakov'

import bpy
from bpy.props import StringProperty
import collections


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





class OperatorTemplateMixin(object):
    bl_options = {'REGISTER', 'UNDO'}

    @property
    def bl_idname(self):
        return '.'.join(('object', slugify(self.bl_name)))


class BatchOperatorMixin(object):
    """
    Base class for batch processing objects
    Inheritors must override:
        filter_object method to define what objects to process
        process_object method to define what to do with each object
    """
    bl_options = {'REGISTER', 'UNDO'}

    use_selected_objects = True

    def execute(self, context):
        """
        Template method pattern
        Must override filter_object and process_object
        """
        # Select and filter objects
        if self.use_selected_objects:
            objects = context.selected_objects
        else:
            drop_selection(context.scene)
            objects = context.scene.objects
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
        """
        If you need obj - return True
        """
        return True

    def process_object(self, obj):
        """
        Hey! You must redefine me!
        Here is most work will be
        """
        raise NotImplementedError


def batch_operator_factory(operator_name, name, filter_func, process_func, use_selected_objects=True):
    bl_idname = '.'.join(('object', slugify(name)))
    return type(operator_name, (BatchOperatorMixin, bpy.types.Operator), {'bl_label': name,
                                                                          'bl_idname': bl_idname,
                                                                          'filter_object': filter_func,
                                                                          'process_object': process_func,
                                                                          'use_selected_objects': use_selected_objects, })


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
