# -*- coding: utf-8 -*-

bl_info = {
    'name': '1D_Bargool tools',
    'author': 'Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)',
    'category': 'Object',
    'version': (1, 1, 0),
    'location': 'View3D > Toolbar',
}

import bpy
from . import selectors, import_cleanup, prop_matchers
from . import removers, panels
from .settings import BatchOperatorSettings, BatchPanelSettings


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_operator_settings = bpy.props.PointerProperty(
        type=BatchOperatorSettings)
    bpy.types.Scene.batch_panel_settings = bpy.props.PointerProperty(
        type=BatchPanelSettings)


def unregister():
    del bpy.types.Scene.batch_operator_settings
    del bpy.types.Scene.batch_panel_settings
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()