# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy


class BatchSetPanel(bpy.types.Panel):
    bl_label = "1D-Bargool Tools"
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

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        self.scene = scene

        # Select verticals
        layout.prop(
            self.props, 'do_show_select_verticals',
            text='Select vertices',
            icon=self.get_arrow_icon_name('do_show_select_verticals'),
            )

        if self.props.do_show_select_verticals:
            box = layout.box()
            box.operator('mesh.select_verticals')
            box.prop(scene.batch_operator_settings,
                        'verticals_select_behaviour',
                        text='Options')
            box.prop(scene.batch_operator_settings,
                        'select_global_limit')

        # Batch remover
        layout.prop(
            self.props, 'do_show_remover',
            text='Batch Remover',
            icon=self.get_arrow_icon_name('do_show_remover'),
            )

        if self.props.do_show_remover:
            box = layout.box()
            box.operator(scene.batch_operator_settings.removers_dropdown,
                            text='Remove')
            box.prop(scene.batch_operator_settings, 'removers_dropdown',
                        text='Action')
            box.prop(scene.batch_operator_settings, 'work_without_selection')

        # Object import cleanup
        layout.prop(self.props,
                    'do_show_cleanup',
                    text='Obj Import Cleanup',
                    icon=self.get_arrow_icon_name('do_show_cleanup'))
        if self.props.do_show_cleanup:
            box = layout.box()
            box.operator('mesh.import_cleanup')
            box.prop(scene.batch_operator_settings,
                        'import_cleanup_recalculate_normals')

        # Misc
        layout.prop(self.props,
                    'do_show_misc',
                    text='Obj Import Cleanup',
                    icon=self.get_arrow_icon_name('do_show_misc'))
        if self.props.do_show_misc:
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