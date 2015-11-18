# -*- coding: utf-8 -*-
import bpy

from Bargool_1D_tools.removers import create_panel_rems
from . import naming, import_utils

__author__ = 'Aleksey Nakoryakov'


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
        split = layout.split()
        split.prop(
            self.props, prop_name,
            text=text,
            icon=self.get_arrow_icon_name(prop_name),
            )
        prop_value = getattr(self.props, prop_name, False)
        return prop_value

    def draw(self, context):
        scene = context.scene
        self.scene = scene
        layout = self.layout
        top_col = layout.column(align=True)

        # Select vertices
        if self.do_create_subpanel(top_col, 'do_show_select_vertices', 'Select vertices'):
            box = top_col.box()
            col = box.column(align=True)
            col.operator('mesh.select_vertices')
            col.prop(scene.batch_operator_settings,
                     'verticals_select_behaviour',
                     text='Options')
            col.prop(scene.batch_operator_settings,
                     'select_global_limit')

        # Batch remover
        if self.do_create_subpanel(top_col, 'do_show_remover', 'Batch Remover'):
            box = top_col.box()
            col = box.column(align=True)
            create_panel_rems(col, scene)

        # Object import cleanup
        if self.do_create_subpanel(top_col, 'do_show_cleanup', 'Obj Import Cleanup'):
            box = top_col.box()
            col = box.column(align=True)
            import_utils.create_panel(col, scene)

        # Instances Placement
        if self.do_create_subpanel(top_col, 'do_show_instances_placement', 'Instances Placement'):
            box = top_col.box()
            col = box.column(align=True)

            operators = [
                'object.import_instances',
                'object.find_instances',
                'object.select_instances',
                'object.deselect_instances',
                'object.drop_instances',
                'object.instances_to_cursor',
                ]
            for op in operators:
                col.operator(op)

        # Naming Tools
        if self.do_create_subpanel(top_col, 'do_show_naming_tools', 'Naming Tools'):
            box = top_col.box()
            col = box.column(align=True)
            naming.create_panel(col)

        # Misc
        if self.do_create_subpanel(top_col, 'do_show_misc', 'Misc'):
            box = top_col.box()
            col = box.column(align=True)
            operators = [
                'object.material_slot_assign',
                'object.isolate_layers',
                'object.match_draw_type',
                'object.match_hide_render',
                'object.select_same_hide_render',
                ''
                ]
            for op in operators:
                col.operator(op)
