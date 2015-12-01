# -*- coding: utf-8 -*-
import bpy

__author__ = 'Aleksey Nakoryakov'


class RunCurrentScriptOperator(bpy.types.Operator):
    bl_idname = 'object.run_current_script'
    bl_label = 'Run Current Script'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        area = [a for a in context.screen.areas if a.type == 'TEXT_EDITOR'][0]
        text = area.spaces.active.text
        ctx = context.copy()
        ctx['edit_text'] = text
        bpy.ops.text.run_script(ctx)
        return {'FINISHED'}


class SaveAndRunScriptOperator(bpy.types.Operator):
    bl_idname = 'object.save_and_run_script'
    bl_label = 'Save and Run Current Script'
    bl_options = {'REGISTER', 'UNDO'}

    class OPERATOR_TYPE_ENUM:
        do_save = 'DO_SAVE'
        do_execute = 'DO_EXECUTE'

    operator_type = bpy.props.EnumProperty(items=((OPERATOR_TYPE_ENUM.do_execute,) * 3,
                                                  (OPERATOR_TYPE_ENUM.do_save,) * 3),
                                           options={'HIDDEN'})

    def execute(self, context):
        if self.operator_type == self.OPERATOR_TYPE_ENUM.do_save:
            area = [a for a in context.screen.areas if a.type == 'TEXT_EDITOR'][0]
            context.scene.test_props.text = area.spaces.active.text
            self.report({'INFO'}, "Saved")
        elif self.operator_type == self.OPERATOR_TYPE_ENUM.do_execute:
            ctx = context.copy()
            ctx['edit_text'] = context.scene.test_props.text
            bpy.ops.text.run_script(ctx)
            self.report({'INFO'}, "Run")
        return {'FINISHED'}


def create_panel(col, scene):
    operators = [
        'object.material_slot_assign',
        'object.isolate_layers',
        'object.match_draw_type',
        'object.match_hide_render',
        'object.select_same_hide_render',
        'object.run_current_script',
        ]
    for op in operators:
        col.operator(op)
    col.operator('object.save_and_run_script',
                 text='Remember script').operator_type = SaveAndRunScriptOperator.OPERATOR_TYPE_ENUM.do_save
    col.operator('object.save_and_run_script',
                 text='Run script').operator_type = SaveAndRunScriptOperator.OPERATOR_TYPE_ENUM.do_execute
