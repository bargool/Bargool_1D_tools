# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

from collections import namedtuple
import bpy
import bmesh
from . import utils


class VerticalVerticesSelectOperator(bpy.types.Operator):
    bl_idname = 'mesh.select_vertices'
    bl_label = 'Select vertices'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    @classmethod
    def get_selected_verts(cls, context, bm=None):
        if not bm:
            obj = context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
        selected = [(v.co.x, v.co.y, v.co.z) for v in bm.verts if v.select]
        if not selected:
            return None
        seldict = {}
        for x, y, z in selected:
            if (x, y) in seldict:
                seldict[(x, y)].append(z)
            else:
                seldict[(x, y)] = [z, ]
        Vertex = namedtuple('Vertex', ['x', 'y', 'zs', 'zmin', 'zmax'])  # zs - list of zeds =)
        result_coords = [
            Vertex(x=xy[0], y=xy[1], zs=z, zmin=min(z), zmax=max(z))
            for xy, z in seldict.items()]

        global_limit = context.scene.batch_operator_settings.select_global_limit
        if global_limit:
            zmin = min(x.zmin for x in result_coords)
            zmax = max(x.zmax for x in result_coords)
            result_coords = [Vertex(x=v.x, y=v.y, zs=v.zs, zmin=zmin, zmax=zmax)
                             for v in result_coords]
        return result_coords

    def execute(self, context):
        threshold = context.scene.tool_settings.double_threshold
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        selected = self.get_selected_verts(bm=bm, context=context)
        if not selected:
            self.report({'INFO'}, 'Must select vertices previously')
            return {'CANCELLED'}
        count = 0

        settings = context.scene.batch_operator_settings
        behaviour = settings.verticals_select_behaviour

        if behaviour == 'Z Between':
            faces_count = 0
            for f in bm.faces:
                if f.select:
                    faces_count += 1
            if faces_count == 1:
                behaviour = 'Z All'

        if behaviour == 'Z All':
            fitness_func = lambda vert: [
                v for v in selected
                if (abs(vert.co.x - v.x) < threshold
                    and abs(vert.co.y - v.y) < threshold)]
        elif behaviour == 'Z Up':
            fitness_func = lambda vert: [
                v for v in selected
                if (abs(vert.co.x - v.x) < threshold
                    and abs(vert.co.y - v.y) < threshold
                    and v.zmin - vert.co.z < threshold)]
        elif behaviour == 'Z Down':
            fitness_func = lambda vert: [
                v for v in selected
                if (abs(vert.co.x - v.x) < threshold
                    and abs(vert.co.y - v.y) < threshold
                    and vert.co.z - v.zmax < threshold)]
        elif behaviour == 'Z Between':
            fitness_func = lambda vert: [
                v for v in selected
                if (abs(vert.co.x - v.x) < threshold
                    and abs(vert.co.y - v.y) < threshold
                    and vert.co.z - v.zmax < threshold
                    and v.zmin - vert.co.z < threshold)]
        elif behaviour == 'Z Level':
            global_limit = context.scene.batch_operator_settings.select_global_limit

            if global_limit:
                zmin, zmax = min(x.zmin for x in selected), max(
                    x.zmax for x in selected)
                fitness_func = lambda vert: [
                    v for v in selected
                    if (vert.co.z - zmax < threshold
                        and zmin - vert.co.z < threshold)]
            else:
                selected_z = frozenset([z for v in selected for z in v.zs])
                fitness_func = lambda vert: [
                    z for z in selected_z
                    if z - threshold < vert.co.z < z + threshold]

        for vert in bm.verts:
            if not vert.hide and fitness_func(vert):
                count += 1
                vert.select = True
        # Remember previous selection mode. We will restore it later
        select_mode = context.tool_settings.mesh_select_mode[:]
        # Force blender show selected vertices
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        # Return to previous select_mode
        context.tool_settings.mesh_select_mode = select_mode
        message = 'Selected {0} vertices'.format(count)
        self.report({'INFO'}, message)

        return {'FINISHED'}


class SelectInstancesOperator(bpy.types.Operator):
    bl_idname = 'object.select_instances'
    bl_label = 'Select Instances'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        scene = context.scene
        selected_objects = context.selected_objects
        mesh_names = set([o.data.name for o in selected_objects])
        objects_to_select = [obj for obj in scene.objects if obj.data.name in mesh_names]
        for obj in objects_to_select:
            obj.select = True
        return {'FINISHED'}


class DeselectInstancesOperator(utils.BatchOperatorMixin, bpy.types.Operator):
    bl_idname = 'object.deselect_instances'
    bl_label = 'Deselect Instances'

    def filter_object(self, obj):
        return obj.data.users > 1

    def process_object(self, obj):
        obj.select = False