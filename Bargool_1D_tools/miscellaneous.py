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


class BatchUnionOperator(bpy.types.Operator):
    bl_idname = 'object.batch_union'
    bl_label = 'Bool Multi Union'

    def execute(self, context):
        obj = context.active_object
        if obj.data.users > 1:
            self.report({'ERROR'}, 'Active is multiuser data object')
            return {'CANCELLED'}
        do_triangulate = context.scene.batch_operator_settings.do_triangulate_while_union
        scene = context.scene
        if do_triangulate:
            for o in context.selected_objects:
                # Only in edge select
                # bpy.ops.mesh.select_non_manifold()
                scene.objects.active = o
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.quads_convert_to_tris()
                bpy.ops.object.mode_set(mode='OBJECT')

        scene.objects.active = obj
        selected_objects = [o for o in context.selected_objects if o != obj]
        for o in selected_objects:
            bpy.ops.object.modifier_add(type='BOOLEAN')
            obj.modifiers["Boolean"].operation = 'UNION'
            obj.modifiers["Boolean"].object = o
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
            if do_triangulate:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.quads_convert_to_tris()
                bpy.ops.object.mode_set(mode='OBJECT')
        obj.select = False
        bpy.ops.object.delete()
        obj.select = True
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

    box = col.box().column(align=True)
    box.operator(BatchUnionOperator.bl_idname)
    box.prop(scene.batch_operator_settings,
             'do_triangulate_while_union')
    for op in operators:
        col.operator(op)
    col.operator('object.save_and_run_script',
                 text='Remember script').operator_type = SaveAndRunScriptOperator.OPERATOR_TYPE_ENUM.do_save
    col.operator('object.save_and_run_script',
                 text='Run script').operator_type = SaveAndRunScriptOperator.OPERATOR_TYPE_ENUM.do_execute
