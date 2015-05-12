# -*- coding: utf-8 -*-

bl_info = {
    'name': '1D-Bargool tools',
    'author': 'Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)',
    'category': 'Object',
    'version': (1, 0, 0),
    'location': 'View3D > Toolbar',
}

import bpy
from batch_set import selectors, import_cleanup, prop_matchers
from batch_set import removers, panels
from batch_set.settings import BatchOperatorSettings, BatchPanelSettings


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_operator_settings = bpy.props.PointerProperty(
        type=BatchOperatorSettings)
    bpy.types.Scene.batch_panel_settings = bpy.props.PointerProperty(
        type=BatchPanelSettings)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()