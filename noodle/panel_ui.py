import bpy
from bpy.types import Menu, Panel
from .config import *
from . import globals

from math import *

class PhysicButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (context.object) and (not rd.use_game_engine)


class PHYSICS_PT_implicit(PhysicButtonsPanel, Panel):
    bl_label = "Noodle Surfaces"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        layout.prop(ob.implicit, "surface_groups")
        layout.prop(ob.implicit, "blend_mode")
        layout.prop(ob.implicit, "node_tree")
        layout.prop(ob.implicit, "global_mode")


from . import utils
globals.module_registrar.add(utils.Registrar([
  PHYSICS_PT_implicit
]))

