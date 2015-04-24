# -*- coding: utf-8 -*-

bl_info = {
    'name': 'Batch Set',
    'author': 'Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)',
    'category': 'Object',
    'version': (0, 11, 0),
    'location': 'View3D > Toolbar',
}

import bpy
from batch_set import selectors, import_cleanup, prop_matchers
from batch_set import removers, panels
from batch_set.settings import BatchOperatorSettings


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_operator_settings = bpy.props.PointerProperty(
        type=BatchOperatorSettings)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()