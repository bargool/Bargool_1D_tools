__author__ = 'Alexey.Nakoryakov'

from bpy.props import StringProperty


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