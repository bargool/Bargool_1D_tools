# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy


class ImportCleanupOperator(bpy.types.Operator):
    """ Class by Paul Kotelevets """
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

        return {'FINISHED'}