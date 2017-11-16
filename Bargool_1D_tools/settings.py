from operator import attrgetter

import bpy

from .removers import BatchRemoverMixin

__author__ = 'Aleksey Nakoryakov'


def get_description(operator):
    """ Gets description from operator, if exists """
    return hasattr(operator, 'bl_description') and operator.bl_description


class BatchOperatorSettings(bpy.types.PropertyGroup):
    work_without_selection = bpy.props.BoolProperty(
        name='Work without selection',
        default=False,
        description='If set, batch erasers will'
                    ' work with all objects without selection')

    # We need all subclasses of BatchRemoverMixin in one dropdown
    operators = [
        (op.bl_idname, op.dropdown_name, get_description(op))
        for op in sorted(BatchRemoverMixin.__subclasses__(), key=attrgetter('dropdown_name'))]

    removers_dropdown = bpy.props.EnumProperty(
        items=operators,
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

    select_global_limit = bpy.props.BoolProperty(name='Global limit',
                                                 default=True)

    import_cleanup_recalculate_normals = bpy.props.BoolProperty(
        name='Recalculate Normals', default=False)
    import_cleanup_apply_rotations = bpy.props.BoolProperty(
        name='Apply rotation', default=True)
    import_cleanup_remove_doubles = bpy.props.BoolProperty(
        name='Remove doubles', default=True)
    import_cleanup_remove_doubles_threshold = bpy.props.FloatProperty(
        name='threshold', default=0.001, precision=4,
        min=0.0001, max=10
    )
    import_cleanup_tris_to_quads = bpy.props.BoolProperty(
        name='Tris to quads', default=True)
    import_cleanup_tris_to_quads_limit = bpy.props.IntProperty(
        name='limit', default=60, min=0, max=360
    )
    import_cleanup_clear_custom_normals = bpy.props.BoolProperty(
        name='Clear custom normals',
        default=True,
    )
    import_cleanup_reveal_hidden = bpy.props.BoolProperty(
        name='Reveal hidden',
        default=True,
    )
    import_cleanup_fix_double_faces = bpy.props.BoolProperty(
        name='Fix Double Faces',
        default=False,
    )
    import_cleanup_triangulate = bpy.props.BoolProperty(
        name='Triangulate',
        default=False,
    )
    geometry_inbound_only = bpy.props.BoolProperty(
        name='Inbound Only', default=True)

    do_triangulate_while_union = bpy.props.BoolProperty(name='Do triangulate',
                                                        default=True)


class TestSettings:
    text = None
    slope_plane = None


class BatchPanelSettings(bpy.types.PropertyGroup):
    do_show_select_vertices = bpy.props.BoolProperty(default=False)
    do_show_remover = bpy.props.BoolProperty(default=False)
    do_show_cleanup = bpy.props.BoolProperty(default=False)
    do_show_misc = bpy.props.BoolProperty(default=False)
    do_show_instances_placement = bpy.props.BoolProperty(default=False)
    do_show_naming_tools = bpy.props.BoolProperty(default=False)
    do_show_slope_align = bpy.props.BoolProperty(default=False)
