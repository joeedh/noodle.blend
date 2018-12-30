import bpy
from bpy.types import NodeTree, Node, NodeSocket
from . import globals

from . import node, node_categories, utils
from .config import *
import nodeitems_utils

import imp;

def register_tree():
    from .node import NoodleTree
    from bpy.utils import register_class
    
    register_class(NoodleTree)
    nodeitems_utils.register_node_categories(NODETREE_TYPE+"_NODES", node_categories.node_categories),
    
def unregister_tree():
    from .node import NoodleTree
    from bpy.utils import unregister_class
    
    nodeitems_utils.unregister_node_categories(NODETREE_TYPE+"_NODES"),
    unregister_class(NoodleTree)

#categories have to be registered after the nodetree but unregistered before it,
#so thus the clunkyness here
globals.module_registrar.add(utils.Registrar([
  utils.Registrar.custom(register_tree, unregister_tree)
]))
