import bpy
from . import (selectors, import_utils, prop_matchers, geometry,
               removers, panels, instances, naming, miscellaneous, utils)
from .settings import BatchOperatorSettings, BatchPanelSettings, TestSettings

__author__ = 'Aleksey Nakoryakov'


bl_info = {
    "blender": (2, 76, 1),
    "name": "Bargool_1D tools",
    "description": "",
    "author": "Aleksey Nakoryakov, Paul Kotelevets aka 1D_Inc (concept design)",
    "category": "Object",
    "version": (1, 8, 6),
    "location": "View3D > Toolbar",
    "wiki_url": "https://github.com/bargool/Bargool_1D_tools",
    "tracker_url": "https://github.com/bargool/Bargool_1D_tools/issues",
}


def reload_modules():
    import importlib
    for m in [selectors, import_utils, prop_matchers,
              removers, panels, settings,
              instances, naming, miscellaneous,
              geometry, utils]:
        importlib.reload(m)


def register():
    reload_modules()
    bpy.utils.register_module(__name__)
    bpy.types.Scene.batch_operator_settings = bpy.props.PointerProperty(
        type=BatchOperatorSettings)
    bpy.types.Scene.batch_panel_settings = bpy.props.PointerProperty(
        type=BatchPanelSettings)
    bpy.types.Scene.test_props = TestSettings


def unregister():
    if hasattr(bpy.types.Scene, 'batch_operator_settings'):
        del bpy.types.Scene.batch_operator_settings
    if hasattr(bpy.types.Scene, 'batch_panel_settings'):
        del bpy.types.Scene.batch_panel_settings
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()
