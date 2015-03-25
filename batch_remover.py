# -*- coding: utf-8 -*-   

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    'name': 'Batch Remover',
    'author': 'Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)',
    'category': 'Object',
    'version': (0, 9, 0),
    'location': 'View3D > Toolbar',
    'category': 'Mesh'
}

import bpy
import bmesh
from collections import namedtuple


class BaseBatchOperator(object):
    """
    Base operator for batch processing objects
    Inheritors must override:
        filter_object method to define what objects to process
        process_object method to define what to do with each object
    """
    bl_options = { 'REGISTER', 'UNDO' }
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects or context.scene.batch_operator_settings.work_without_selection
    
    def execute(self, context):
        """
        Template method pattern
        Must override filter_object and process_object
        """
        # Count is just for debug stuff
        count = 0
        # Select and filter objects
        objects = context.selected_objects or bpy.data.objects
        work_objects = [obj for obj in objects if self.filter_object(obj)]
        # Cache old active object. At the end we will return activeness
        old_active = bpy.context.scene.objects.active
        for obj in work_objects:
            # As I understood, objects for bpy.ops operators must be
            # active in most cases
            bpy.context.scene.objects.active = obj
            # Fight!
            count += self.process_object(obj)
        bpy.context.scene.objects.active = old_active

        message = 'Removed {0} properties'.format(count)
        self.report({'INFO'}, message)

        return {'FINISHED'}
    
    def filter_object(self, obj):
        """
        Hey! You must redefine me!
        If you need obj - return True
        """
        raise NotImplementedError
    
    def process_object(self, obj):
        """
        Hey! You must redefine me!
        Here is most work will be
        """
        raise NotImplementedError


class BatchUVMapsEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.uvmaps_eraser'
    bl_label = 'UV Maps Batch Remove'
    bl_description = 'Removes UV Maps from selected or all objects in scene'
    dropdown_name = 'UV Maps'
    
    def filter_object(self, obj):
        """ We need to remove uv_textures. So we need objects with them """
        # I didn't see blender yet, so I don't know what objects have textures, so just find them
        return hasattr(obj.data, 'uv_textures')
    
    def process_object(self, obj):
        count = 0
        while obj.data.uv_textures:
                bpy.ops.mesh.uv_texture_remove()
                count += 1
        return count


class BatchVertexGroupEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.vertex_groups_eraser'
    bl_label = 'Vertex Groups Batch Remove'
    bl_description = 'Removes Vertex Groups from selected or all objects in scene'
    dropdown_name = 'Vertex Groups'
    
    def filter_object(self, obj):
        has_groups = hasattr(obj, 'vertex_groups') and len(obj.vertex_groups) > 0
        return has_groups
    
    def process_object(self, obj):
        bpy.ops.object.vertex_group_remove(all=True)
        # We try to count removed items, so return something
        return 1
    
    
class BatchShapeKeysEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.shape_keys_eraser'
    bl_label = 'Shape Keys Batch Remove'
    bl_description = 'Removes Shape Keys from selected or all objects in scene'
    dropdown_name = 'Shape Keys'
    
    def filter_object(self, obj):
        has_keys = hasattr(obj.data, 'shape_keys') and obj.data.shape_keys
        return True if has_keys else False
    
    def process_object(self, obj):
        bpy.ops.object.shape_key_remove(all=True)
        # We try to count removed items, so return something
        return 1


class BatchVertexColorsEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.vertex_colors_eraser'
    bl_label = 'Vertex Colors Batch Remove'
    bl_description = 'Removes VCols from selected or all objects in scene'
    dropdown_name = 'Vertex Colors'
    
    def filter_object(self, obj):
        has_colors = hasattr(obj.data, 'vertex_colors') and obj.data.vertex_colors
        return True if has_colors else False
    
    def process_object(self, obj):
        count = 0
        while obj.data.vertex_colors:
                for color in obj.data.vertex_colors:
                    # Have to make vcolor active to remove it
                    color.active = True
                    bpy.ops.mesh.vertex_color_remove()
                    # count is wrong because there is no guarantee that 
                    # vertex_color_remove tries to our active color
                    count += 1
        return count
    
    
class BatchMaterialEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.materials_eraser'
    bl_label = 'Materials Batch Remove'
    bl_description = 'Removes Materials from selected or all objects in scene'
    dropdown_name = 'Materials'
    
    def filter_object(self, obj):
        has_materials = hasattr(obj.data, 'materials') and obj.data.materials
        return True if has_materials else False
    
    def process_object(self, obj):
        count = 0
        while obj.data.materials:
            bpy.ops.object.material_slot_remove()
            count += 1
        return count
    
    
class BatchGPencilEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.gpencil_eraser'
    bl_label = 'GPencil Batch Remove'
    bl_description = 'Removes GPencils from selected or all objects in scene'
    dropdown_name = 'Grease Pencil'
    
    def filter_object(self, obj):
        has_materials = hasattr(obj, 'grease_pencil') and obj.grease_pencil
        return True if has_materials else False
    
    def process_object(self, obj):
        count = 0
        while obj.grease_pencil:
            bpy.ops.gpencil.data_unlink()
            count += 1
        return count


class AllModifiersEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.all_modifiers_eraser'
    bl_label = 'All Modifiers Batch Remove'
    bl_description = 'Removes All Modifiers from selected or all objects in scene'
    dropdown_name = 'All Modifiers'
    
    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and len(obj.modifiers) > 0
        return True if has_modifiers else False
    
    def process_object(self, obj):
        count = 0
        for modifier in obj.modifiers:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class AllSubsurfsEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.all_subsurfs_eraser'
    bl_label = 'All Subsurfs Batch Remove'
    bl_description = 'Removes All Subsurfs from selected or all objects in scene'
    dropdown_name = 'All Subsurfs'
    
    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and len(obj.modifiers) > 0
        return True if has_modifiers else False
    
    def process_object(self, obj):
        count = 0
        subsurfs = [m for m in obj.modifiers if m.type == 'SUBSURF']
        for modifier in subsurfs:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class ZeroSubsurfsEraserOperator(BaseBatchOperator, bpy.types.Operator):
    bl_idname = 'object.zero_subsurfs_eraser'
    bl_label = 'Zero Subsurfs Batch Remove'
    bl_description = 'Removes Subsurfs with view 0 from selected or all objects in scene'
    dropdown_name = 'Zero Subsurfs'
    
    def filter_object(self, obj):
        has_modifiers = hasattr(obj, 'modifiers') and len(obj.modifiers) > 0
        return True if has_modifiers else False
    
    def process_object(self, obj):
        count = 0
        subsurfs = [m for m in obj.modifiers if m.type == 'SUBSURF' and m.levels == 0]
        for modifier in subsurfs:
            bpy.ops.object.modifier_remove(modifier=modifier.name)
            count += 1
        return count


class VerticalVerticesSelectOperator(bpy.types.Operator):
    bl_idname = 'mesh.select_verticals'
    bl_label = 'Select verticals'
    bl_options = { 'REGISTER', 'UNDO' }
    
    @classmethod
    def poll(cls, context):
        is_mesh_mode = context.mode == 'EDIT_MESH'
        return is_mesh_mode
    
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
            if (x,y) in seldict:
                seldict[(x, y)].append(z)
            else:
                seldict[(x, y)] = [z, ]
        Vertex = namedtuple('Vertex', ['x', 'y', 'zmin', 'zmax'])
        result_coords = [
            Vertex(x=xy[0], y=xy[1], zmin=min(z), zmax=max(z))
            for xy, z in seldict.items()]
            
        global_limit = context.scene.batch_operator_settings.select_global_limit
        if global_limit:
            zmin, zmax = min(x.zmin for x in result_coords), max(x.zmax for x in result_coords)
            result_coords = [Vertex(x=v.x, y=v.y, zmin=zmin, zmax=zmax) for v in result_coords]
        print(result_coords)
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
        
        behaviour = context.scene.batch_operator_settings.verticals_select_behaviour
            
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
            zmin, zmax = min(x.zmin for x in selected), max(x.zmax for x in selected)
            fitness_func = lambda vert: [
                v for v in selected
                    if (vert.co.z - zmax < threshold
                    and zmin - vert.co.z < threshold)]
        
        for vert in bm.verts:
            if not vert.hide and fitness_func(vert):
                count += 1
                vert.select = True
        # Force blender show selected vertices
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        message = 'Selected {0} vertices'.format(count)
        self.report({'INFO'}, message)

        return {'FINISHED'}

class ImportCleanupOperator(bpy.types.Operator):
    """ Class by Paul Kotelevets """
    bl_idname = 'mesh.import_cleanup'
    bl_label = 'Obj Import Cleanup'
    bl_options = { 'REGISTER', 'UNDO' }
    
    def execute(self, context):
        mallas = [o for o in objetos if o.type == 'MESH' and o.is_visible(scn)]
        obj= context.selected_objects
        for ob in obj:
            if ob.type == 'MESH':
                ob.select = True
                context.scene.objects.active = ob
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)
                bpy.ops.mesh.tris_convert_to_quads(limit=0.698132, uvs=False, vcols=False, sharp=False, materials=False)
                # remove uvs
                bpy.ops.mesh.normals_make_consistent(inside=False )
                bpy.ops.object.mode_set(mode='OBJECT')

def get_description(operator):
    """ Gets description from operator, if exists """
    return hasattr(operator, 'bl_description') and operator.bl_description


class BatchOperatorSettings(bpy.types.PropertyGroup):
    work_without_selection = bpy.props.BoolProperty(
        name='Work without selection',
        default=False,
        description='If set, batch erasers will work with all objects without selection')

    # We need subclass of BaseBatchOperator in one dropdown
    operators = [
        (op.bl_idname, op.dropdown_name, get_description(op))
        for op in BaseBatchOperator.__subclasses__()]
        
    removers_dropdown = bpy.props.EnumProperty(
        items= operators,
        name='Removers')
    
    # TODO: Extract this and next to another class. Just for verticals
    verticals_select_behaviour = bpy.props.EnumProperty(
        items=[
            ('Z All', 'All', 'Z All'),
            ('Z Up', 'Up', 'Z Up'),
            ('Z Down', 'Down', 'Z Down'),
            ('Z Between', 'Between', 'Z Between'),
            ('Z Level', 'Z Level', 'Z Level'),
        ],
        name='Options')
    
    select_global_limit = bpy.props.BoolProperty(name='Global limit', default=True)


class RemoverPanel(bpy.types.Panel):
    bl_label = "Batch Remover"
    bl_idname = "SCENE_PT_remover"
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
            row.operator(op)

        layout.separator()
        row = layout.row()
        row.prop(scene.batch_operator_settings, 'work_without_selection')
        row = layout.row(align=True)
        row.operator(scene.batch_operator_settings.removers_dropdown, text='Remove')
        row = layout.row(align=True)
        row.prop(scene.batch_operator_settings, 'removers_dropdown', text='Action')
        # For dropdown look at http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Interface
        row = layout.row(align=True)
        op = row.operator('mesh.select_verticals')
        row = layout.row(align=True)
        row.prop(scene.batch_operator_settings, 'verticals_select_behaviour', text='Options')
        row = layout.row(align=True)
        row.prop(scene.batch_operator_settings, 'select_global_limit')
        row = layout.row()
        row.operator('mesh.import_cleanup')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_operator_settings = bpy.props.PointerProperty(type=BatchOperatorSettings)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()