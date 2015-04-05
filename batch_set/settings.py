# -*- coding: utf-8 -*-

__author__ = 'Aleksey Nakoryakov'

import bpy
from batch_set.removers import BaseBatchRemover


def get_description(operator):
    """ Gets description from operator, if exists """
    return hasattr(operator, 'bl_description') and operator.bl_description


class BatchOperatorSettings(bpy.types.PropertyGroup):
    work_without_selection = bpy.props.BoolProperty(
        name='Work without selection',
        default=False,
        description='If set, batch erasers will'
                    ' work with all objects without selection')

    # We need all subclasses of BaseBatchRemover in one dropdown
    operators = [
        (op.bl_idname, op.dropdown_name, get_description(op))
        for op in BaseBatchRemover.__subclasses__()]

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