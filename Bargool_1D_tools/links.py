__author__ = 'alexey.nakoryakov'

import bpy


def get_link_filepath(obj):
    return obj.data.library.filepath if obj.data.library else None


def find_same_link(scene, obj):
    link_filepath = get_link_filepath(obj)
    if link_filepath:
        return [o for o in scene.objects if get_link_filepath(o) == link_filepath]


class SelectLinkedOperator(bpy.types.Operator):
    bl_idname = 'object.select_linked_objects'
    bl_label = 'Select Linked objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        same_links = find_same_link(context.scene, active)
        if same_links:
            for o in context.selected_objects:
                o.select = False
            for o in same_links:
                o.select = True

        return {'FINISHED'}


class DetachLinked(bpy.types.Operator):
    bl_idname = 'object.delete_linked_object'
    bl_label = 'Delete Linked objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active = context.active_object
        scene = context.scene
        same_links = find_same_link(scene, active)
        if same_links:
            for o in same_links:
                scene.objects.active = o
                bpy.ops.object.proxy_make()
                bpy.ops.object.delete(use_global=False)
        return {'FINISHED'}