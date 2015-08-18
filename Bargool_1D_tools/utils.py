__author__ = 'Alexey.Nakoryakov'

from bpy.props import StringProperty
import collections


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


