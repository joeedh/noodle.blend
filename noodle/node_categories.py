import bpy
from bpy.types import NodeTree, Node, NodeSocket, Operator
from bl_operators.node import NodeAddOperator
from .config import *
from . import globals

### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

from . import utils, node
from .node import *


class NoodleNodeItem (NodeItem):
    def __init__(self, nodetype, label=None, settings=None, poll=None, tree_name=""):

        if settings is None:
            settings = {}

        self.tree_name = tree_name
        self.nodetype = nodetype
        self._label = label
        self.settings = settings
        self.poll = poll

    @property
    def label(self):
        if self._label:
            return self._label
        else:
            # if no custom label is defined, fall back to the node type UI name
            return getattr(bpy.types, self.nodetype).bl_rna.name

    # NB: is a staticmethod because called with an explicit self argument
    # NodeItemCustom sets this as a variable attribute in __init__
    @staticmethod
    def draw(self, layout, context):
        default_context = bpy.app.translations.contexts.default

        props = layout.operator("node.add_"+APIPRE+"group_node", text=self.label, text_ctxt=default_context)
        props.type = self.nodetype
        props.use_transform = True
        props.tree_name = self.tree_name
        props.node_name = self.tree_name
        
        for setting in self.settings.items():
            ops = props.settings.add()
            ops.name = setting[0]
            ops.value = setting[1]

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class NoodleNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == NODETREE_TYPE

def get_groups(unused):
  for ntree in bpy.data.node_groups:
    if ntree.bl_idname != NODETREE_TYPE: continue
    
    nitem = NoodleNodeItem(PRE+"NodeGroup", label=ntree.name, tree_name=ntree.name)
    yield nitem
  
# all categories in a list
node_categories = [
    # identifier, label, items list
    NoodleNodeCategory("OUTPUTS", "Output Nodes", items=[
#       NodeItem("NoodleOutputNode"),
#       NodeItem("NoodleOutputNode"),
        NodeItem(PRE+"NodeGroupOutput"),
        NodeItem(PRE+"MathNode")
    ]),
    NoodleNodeCategory("INPUT", "Input Nodes", items=[
#       NodeItem("NoodleInputNode"),
        NodeItem("NodeGroupInput")
    ]),
    NoodleNodeCategory("GROUPS", "Groups", items=get_groups),
]
