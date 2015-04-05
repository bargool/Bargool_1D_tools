# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy


class BatchSetPanel(bpy.types.Panel):
    bl_label = "Batch Set"
    bl_idname = "SCENE_PT_batchset"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # There was a lot of operators, now last one remain
        operators = [
            'object.material_slot_assign',
        ]
        for op in operators:
            layout.operator(op)

        layout.prop(scene.batch_operator_settings, 'work_without_selection')
        layout.operator(scene.batch_operator_settings.removers_dropdown,
                     text='Remove')
        layout.prop(scene.batch_operator_settings, 'removers_dropdown',
                 text='Action')
        # For dropdown look at http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Interface
        layout.operator('mesh.select_verticals')
        layout.prop(scene.batch_operator_settings, 'verticals_select_behaviour',
                 text='Options')
        layout.prop(scene.batch_operator_settings, 'select_global_limit')
        layout.operator('mesh.import_cleanup')
        layout.prop(scene.batch_operator_settings,
                 'import_cleanup_recalculate_normals')

        layout.operator('object.match_hide_render')
        layout.operator('object.select_same_hide_render')
        layout.operator('object.isolate_layers')
        layout.operator('object.match_draw_type')