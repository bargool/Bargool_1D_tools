# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy


class BatchSetPanel(bpy.types.Panel):
    bl_label = "Bargool_1D Tools"
    bl_idname = "SCENE_PT_batchsetpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = '1D'
    bl_options = {'DEFAULT_CLOSED'}

    @property
    def props(self):
        return self.scene.batch_panel_settings

    def get_arrow_icon_name(self, propname):
        b = getattr(self.props, propname)
        return 'DOWNARROW_HLT' if b else 'RIGHTARROW'

    def do_create_subpanel(self, layout, prop_name, text):
        layout.prop(
            self.props, prop_name,
            text=text,
            icon=self.get_arrow_icon_name(prop_name),
            )
        prop_value = getattr(self.props, prop_name, False)
        return prop_value

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        self.scene = scene

        # Select vertices
        if self.do_create_subpanel(layout, 'do_show_select_vertices', 'Select vertices'):
            box = layout.box()
            box.operator('mesh.select_vertices')
            box.prop(scene.batch_operator_settings,
                     'verticals_select_behaviour',
                     text='Options')
            box.prop(scene.batch_operator_settings,
                     'select_global_limit')

        # Batch remover
        if self.do_create_subpanel(layout, 'do_show_remover', 'Batch Remover'):
            box = layout.box()
            box.operator(scene.batch_operator_settings.removers_dropdown,
                         text='Remove')
            box.prop(scene.batch_operator_settings, 'removers_dropdown',
                     text='Action')
            box.prop(scene.batch_operator_settings, 'work_without_selection')

        # Object import cleanup
        if self.do_create_subpanel(layout, 'do_show_cleanup', 'Obj Import Cleanup'):
            box = layout.box()
            box.operator('mesh.import_cleanup')
            box.prop(scene.batch_operator_settings,
                     'import_cleanup_recalculate_normals')

        # Misc
        if self.do_create_subpanel(layout, 'do_show_misc', 'Misc'):
            box = layout.box()
            operators = [
                'object.material_slot_assign',
                'object.isolate_layers',
                'object.match_draw_type',
                'object.match_hide_render',
                'object.select_same_hide_render',
                ]
            for op in operators:
                box.operator(op)

        # Instances Placement
        if self.do_create_subpanel(layout, 'do_show_instances_placement', 'Instances Placement'):
            box = layout.box()
            operators = [
                'object.import_instances',
                'object.find_instances',
                'object.select_instances',
                ]
            for op in operators:
                box.operator(op)