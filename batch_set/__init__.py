# -*- coding: utf-8 -*-

bl_info = {
    'name': 'Batch Set',
    'author': 'Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)',
    'category': 'Object',
    'version': (0, 10, 3),
    'location': 'View3D > Toolbar',
}

import bpy
from batch_set.settings import BatchOperatorSettings


def register():
    print(__name__)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_operator_settings = bpy.props.PointerProperty(
        type=BatchOperatorSettings)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()