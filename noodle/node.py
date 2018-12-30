import bpy
from bpy.types import NodeTree, Node, NodeSocket, NodeCustomGroup, NodeGroup, NodeGroupInput
from . import utils
from . import config as cf
from .config import *
from . import globals

# Implementation of custom nodes from Python

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class NoodleTree(NodeTree):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = NODETREE_TYPE
    # Label for nice name display
    bl_label = NODETREE_EDITOR_NAME
    
    # Icon identifier
    bl_icon = 'NODETREE'
  
    @classmethod
    def poll(cls, ntree):
      return True

# Description string
NoodleTree.__doc__ = cf.NODETREE_EDITOR_NAME + " Editor"

class NoodleCustomGroup (NodeCustomGroup):
  bl_idname = PRE+"NodeGroup"
  bl_label = "Group"
  bl_icon = 'SOUND'
  bl_width_min = 250
  
  def init(self, context):
    pass
    
  def copy(self, b):
    pass
    
  def poll_instance(self, tree):
    return ntree.bl_idname == NODETREE_TYPE
    
  @classmethod
  def poll(cls, ntree):
    return ntree.bl_idname == NODETREE_TYPE
    
  # Additional buttons displayed on the node.
  def draw_buttons(self, context, layout):
    if self.node_tree == None:
      return
      
    layout.label(text=self.node_tree.name)
    
    layout.prop(self.node_tree, "name")
    
    prop = layout.operator("node."+APIPRE+"_edit_group", text="Edit Group")
    print("PATH", context.space_data.path[-1].node_tree)
    node_tree = context.space_data.path[-1].node_tree
    prop["node_path"] = utils.gen_node_path(self, node_tree) #context.space_data.path[-1]) #node_tree)
    
  def draw_buttons_ext(self, context, layout):
    pass
      
# Custom socket type
class FieldVectorSocket(NodeSocket):
    # Description string
    '''Vector Socket'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = PRE+'VectorSocket'
    # Label for nice name display
    bl_label = 'Vector'

    value : bpy.props.FloatVectorProperty(default=[0.0, 0.0, 0.0], size=3)
    
    # Optional function for drawing the socket input vector
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=self.name)

    # Socket color
    def draw_color(self, context, node):
        return (0.4, 0.8, 1.0, 1.0)



# Custom socket type
class FieldSocket(NodeSocket):
    # Description string
    '''Value Socket'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = PRE+'FieldSocket'
    # Label for nice name display
    bl_label = 'Field'

    value : bpy.props.FloatProperty(default=0.0)
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=self.name)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 1.0)


  
from . import symbol
sym = symbol.sym

#stype is either 'vec' (vector) or 'field' (scalar)
def coerce(a, stype):
  if type(a) in [list, tuple] and stype != "vec":
    a = sym.func("sqrt", a[0]*a[0] + a[1]*a[1] + a[2]*a[2])
  elif type(a) not in [list, tuple] and stype != "field":
    a = [a, a, a]
  return a
  
# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class NoodleTreeNode:
    tag : bpy.props.IntProperty(default=0) #used during sorting
    
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == NODETREE_TYPE

class math_func_impl:
  def SIN(self, a, b, dva, dvb):
    return sym.func("sin", a)
  def COS(self, a, b, dva, dvb):
    return sym.func("cos", a)
  def TAN(self, a, b, dva, dvb):
    return sym.func("tan", a)#, "{dva}*(tan({a})*tan({a}) + 1.0)"
  def ASIN(self, a, b, dva, dvb):
    return sym.func("asin", a)#, "(-sqrt(-{a}*{a} + 1.0)*{dva})/({a}*{a} - 1.0)"
  def ACOS(self, a, b, dva, dvb):
    return sym.func("acos", a)#, "(sqrt(-{a}*{a} + 1.0)*{dva})/({a}*{a} - 1.0)"
  def POW(self, a, b, dva, dvb):
    return sym.func("pow", [a, b])#, "(pow({a}, {b})*({dva}*{b} + {dvb}*log({a})*{a}))/{a}"
  def ABS(self, a, b, dva, dvb):
    return sym.func("abs", a)
  def FLOOR(self, a, b, dva, dvb):
    return sym.func("floor", a)
  def CEIL(self, a, b, dva, dvb):
    return sym.func("ceil", a)
  def FRACT(self, a, b, dva, dvb):
    return sym.func("fract", a)
  def TRUNC(self, a, b, dva, dvb):
    return sym.func("trunc", a)
  def ATAN(self, a, b, dva, dvb):
    return sym.func("atan", a)#, "atan({a})", "({dva}/({a}*{a}+1.0)"
  def TENT(self, a, b, dva, dvb):
    return sym(1.0) - sym.func("abs", [sym.func("fract", a) - 0.5])*2.0
  def ATAN2(self, a, b, dva, dvb):
    return sym.func("atan2", a)#, "atan2({b}, {a})", "(atan2({a}+0.001) - atan2({a}-0.001)) / 500.0"
  def MUL(self, a, b, dva, dvb):
    return sym(a) * sym(b)
  def SUB(self, a, b, dva, dvb):
    return sym(a) - sym(b)
  def ADD(self, a, b, dva, dvb):
    return sym(a) + sym(b)
  def DIV(self, a, b, dva, dvb):
    return sym(a) / sym(b)
  def MIN(self, a, b, dva, dvb):
    return sym.func("min", [a, b])
  def MAX(self, a, b, dva, dvb):
    return sym.func("max", [a, b])#, "max({a}, {b})", "{a} > {b} ? {dva} : {dvb}"
    
  def CROSS(self, a, b, dva, dvb):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]
    
  #vector functions
  def DOT(self, a, b, dva, dvb):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
  def LEN(self, a, b, dva, dvb):
    return sym.func('sqrt', [a[0]*a[0] + a[1]*a[1] + a[2]*a[2]])
      #"""({dva}[0]*{a}[0] + {dva}[1]*{a}[1] + {dva}[2]*{a}[2]) / 
      #     sqrt({a}[0]*{a}[0] + {a}[1]*{a}[1] + {a}[2]*{a}[2]")"""

#example node
      
# Derived from the Node base type.
class MathNode(Node, NoodleTree):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = PRE+'MathNode'
    # Label for nice name display
    bl_label = 'Math Node'
    # Icon identifier
    bl_icon = 'SOUND'
    bl_width_min = 200
  
    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    #myStringProperty : bpy.props.StringProperty()
    #myFloatProperty : bpy.props.FloatProperty(default=3.1415926)

    # Enum items list
    math_funcs = [
        ("SIN", "Sin", "Sine"),
        ("COS", "Cos", "Cosine"),
        ("TENT", "Tent", "Tent"),
        ("TAN", "Tan", "Tangent"),
        ("ASIN", "Asin", "Sine"),
        ("ACOS", "Acos", "Sine"),
        ("POW", "Pow", "Sine"),
        ("ABS", "Abs", "Sine"),
        ("FLOOR", "Floor", "Sine"),
        ("CEIL", "Floor", "Sine"),
        ("FRACT", "Fract", "Sine"),
        ("TRUNC", "Truncate", "Sine"),
        ("ATAN", "Atan", "Sine"),
        ("ATAN2", "Atan2 (xy to polar)", "Sine"),
        ("MUL", "Multiply", "Sine"),
        ("SUB", "Subtract", "Sine"),
        ("ADD", "Add", "Sine"),
        ("DIV", "Divide", "Sine"),
        ("MIN", "Min", "Min"),
        ("MAX", "Max", "Max"),
    ]
    
    mathFunc : bpy.props.EnumProperty(name="Function", description="Math Functions", items=math_funcs, default='ADD')

    def init(self, context):
        self.inputs.new(PRE+'FieldSocket', "a")
        self.inputs.new(PRE+'FieldSocket', "b")

        self.outputs.new(PRE+'FieldSocket', "field")
    
    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        self.mathFunc = node.mathFunc
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label(text="Node settings")
        layout.prop(self, "mathFunc")
        #layout.prop(self, "myFloatProperty")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        pass
        #layout.prop(self, "myFloatProperty")
        # myStringProperty button will only be visible in the sidebar
        #layout.prop(self, "myStringProperty")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "Math Node"
    
globals.module_registrar.add(utils.Registrar([
  #NoodleTree is registered in node_tree.py
  FieldSocket,
  FieldVectorSocket,
  MathNode,
  NoodleCustomGroup
]));
