# -*- coding: utf-8 -*-

bl_info = {
    "name": "Bargool_1D tools",
    "description": "",
    "author": "Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)",
    "category": "Object",
    "version": (1, 2, 7),
    "location": "View3D > Toolbar",
    "wiki_url": "https://github.com/bargool/Bargool_1D_tools",
    "tracker_url": "https://github.com/bargool/Bargool_1D_tools/issues",
}
import bpy
from . import selectors, import_utils, prop_matchers
from . import removers, panels
from .settings import BatchOperatorSettings, BatchPanelSettings

# Reload all modules
import imp
for m in [selectors, import_utils, prop_matchers, removers, panels, settings]:
    imp.reload(m)


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