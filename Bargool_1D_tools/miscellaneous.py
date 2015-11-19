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
