import math

import bpy

from . import instances

__author__ = 'Aleksey Nakoryakov'


class ImportCleanupOperator(bpy.types.Operator):
    """ Class by Paul Kotelevets, and my little edits """
    bl_idname = 'mesh.import_cleanup'
    bl_label = 'Obj Import Cleanup'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        objects = [o for o in context.selected_objects if
                   o.type == 'MESH' and o.is_visible(scene)]
        settings = context.scene.batch_operator_settings
        for ob in objects:
            ob.select = True
            context.scene.objects.active = ob
            if settings.import_cleanup_fix_double_faces:
                ob.data.validate()
            # transform_apply works only with non-multiuser
            if settings.import_cleanup_apply_rotations and not instances.is_multiuser(ob):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            if settings.import_cleanup_clear_custom_normals:
                bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.mode_set(mode='EDIT')
            if settings.import_cleanup_reveal_hidden:
                bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action='SELECT')
            if settings.import_cleanup_remove_doubles:
                threshold = settings.import_cleanup_remove_doubles_threshold
                bpy.ops.mesh.remove_doubles(threshold=threshold, use_unselected=False)
            if settings.import_cleanup_recalculate_normals:
                bpy.ops.mesh.normals_make_consistent(inside=False)
            if settings.import_cleanup_tris_to_quads:
                limit = math.radians(settings.import_cleanup_tris_to_quads_limit)
                bpy.ops.mesh.tris_convert_to_quads(face_threshold=limit,
                                                   shape_threshold=limit,
                                                   uvs=False,
                                                   vcols=False, sharp=False,
                                                   materials=False)
            bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


def create_panel(col, scene):
    col.operator('mesh.import_cleanup')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_reveal_hidden')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_clear_custom_normals')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_apply_rotations')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_fix_double_faces')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_recalculate_normals')
    col.prop(scene.batch_operator_settings,
             'import_cleanup_remove_doubles')
    sub = col.row()
    sub.active = scene.batch_operator_settings.import_cleanup_remove_doubles
    sub.prop(scene.batch_operator_settings,
             'import_cleanup_remove_doubles_threshold',
             slider=True)
    col.prop(scene.batch_operator_settings,
             'import_cleanup_tris_to_quads')
    sub = col.row()
    sub.active = scene.batch_operator_settings.import_cleanup_tris_to_quads
    sub.prop(scene.batch_operator_settings,
             'import_cleanup_tris_to_quads_limit')
