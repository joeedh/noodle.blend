import traceback

__all__ = [
  "appstate", "config", "event", "node",
  "node_categories", "node_sort", "node_tree",
  "ops", "panel_ui", "props", "symbol", "symbol_factor",
  "symbol_optimize", "utils", "paths", "globals"
];

import imp
from . import paths
import sys, os.path

imp.reload(paths)

from . import config
imp.reload(config)

#add parent directory to python path
from . import paths

#dumb buggy sys.path implementation, it keeps doubling slashes when it normalizes paths
if paths.parentpath not in sys.path and paths.parentpath.replace(os.path.sep, os.path.sep+os.path.sep) not in sys.path:
    print("adding %s to path" % paths.parentpath)
    sys.path.append(paths.parentpath)

config_local = paths.load_parentmodule("noodleconfig", report_error=True)

from . import globals

#unregister old module from blender if it exists
globals.module_registrar.unregister()

if config_local is not None:
    imp.reload(config_local)
    for k in dir(config_local):
        if k.startswith("_"): continue
        
        if hasattr(config, k):
            setattr(config, k, getattr(config_local, k))

if config.APIPRE is None:
    config.APIPRE = config.PRE.lower()

from . import utils
imp.reload(utils)

#create a new Registrar in case utils changed in reloading
globals.module_registrar = utils.Registrar([]);
#globals.module_registrar.clear()

#load main modules

from . import appstate, event, node, node_categories, node_sort, node_tree, \
          ops, panel_ui, props, symbol, symbol_factor, symbol_optimize, utils, paths;


imp.reload(appstate);
imp.reload(event);
imp.reload(appstate);
imp.reload(node_sort);
imp.reload(node_categories);
imp.reload(node_tree);
imp.reload(node);
imp.reload(ops);
imp.reload(panel_ui);
imp.reload(props);
imp.reload(symbol);
imp.reload(symbol_factor);
imp.reload(symbol_optimize);

def register():
    globals.module_registrar.register()
    
def unregister():
    globals.module_registrar.unregister()
    
"""
try:
  node_tree.bpy_exports.unregister()
  ops.bpy_exports.unregister()
  event.bpy_exports.unregister()
  panel_ui.bpy_exports.unregister()
except:
  traceback.print_exc()
  print("Error unregistered add-on")

c_code.close_library()

bpy_exports = utils.Registrar([
  node_tree.bpy_exports,
  ops.bpy_exports,
  props.bpy_exports,
  panel_ui.bpy_exports,
  event.bpy_exports,
])

def register():
  bpy_exports.register()
  
def unregister():
  bpy_exports.unregister()
"""