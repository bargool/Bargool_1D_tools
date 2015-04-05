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
            row = layout.row(align=True)
            layout.operator(op)

        layout.separator()
        row = layout.row()
        row.prop(scene.batch_operator_settings, 'work_without_selection')
        row = layout.row(align=True)
        row.operator(scene.batch_operator_settings.removers_dropdown,
                     text='Remove')
        row = layout.row(align=True)
        row.prop(scene.batch_operator_settings, 'removers_dropdown',
                 text='Action')
        # For dropdown look at http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Interface
        row = layout.row(align=True)
        row.operator('mesh.select_verticals')
        row = layout.row(align=True)
        row.prop(scene.batch_operator_settings, 'verticals_select_behaviour',
                 text='Options')
        row = layout.row(align=True)
        row.prop(scene.batch_operator_settings, 'select_global_limit')
        row = layout.row()
        row.operator('mesh.import_cleanup')
        row = layout.row()
        row.prop(scene.batch_operator_settings,
                 'import_cleanup_recalculate_normals')

        row = layout.row()
        row.operator('object.match_hide_render')
        row = layout.row()
        row.operator('object.select_same_hide_render')
        row = layout.row()
        row.operator('object.isolate_layers')
        row = layout.row()
        row.operator('object.match_draw_type')