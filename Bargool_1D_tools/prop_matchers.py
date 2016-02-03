# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy


class MatchHideRenderOperator(bpy.types.Operator):
    bl_idname = 'object.match_hide_render'
    bl_label = 'Match HideRender'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = context.active_object
        hide_render = active_object.hide_render
        for o in context.selected_objects:
            o.hide_render = hide_render
            o.hide = True

        return {'FINISHED'}


class SelectSameHideRenderOperator(bpy.types.Operator):
    bl_idname = 'object.select_same_hide_render'
    bl_label = 'Select Same HideRender'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        active_object = context.active_object
        hide_render = active_object.hide_render
        same_objects = [o for o in scene.objects if
                        o.hide_render == hide_render]
        for o in same_objects:
            o.select = True

        return {'FINISHED'}


class IsolateLayersOperator(bpy.types.Operator):
    bl_idname = 'object.isolate_layers'
    bl_label = 'Isolate Layers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_layers = [list(o.layers) for o in context.selected_objects]
        layers = map(lambda *x: any(x), *selected_layers)
        scene = context.scene
        scene.layers = list(layers)
        return {'FINISHED'}


class MatchDrawTypeOperator(bpy.types.Operator):
    bl_idname = 'object.match_draw_type'
    bl_label = 'Match DrawType'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = context.active_object
        draw_type = active_object.draw_type
        for o in context.selected_objects:
            o.draw_type = draw_type
        return {'FINISHED'}
