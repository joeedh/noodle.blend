import bpy, bmesh
from math import *
from mathutils import *

from . import codegen
from . import c_code


def generate():
	ob = bpy.context.object
	if ob == None: return
	if ob.name.startswith("__"): return

	from lg.symbol import sym
	from lg import codegen

	#nodetree we'll be working on
	ntree = ob.implicit.node_tree
	if ntree not in bpy.data.node_groups.keys(): return

	from lg import mesh
	
	outname = "__" + ob.name + "_output"
	if outname not in bpy.data.objects.keys():
		outme = bpy.data.meshes.new(outname)
		outobj = bpy.data.objects.new(outname, outme)
		bpy.context.scene.objects.link(outobj)
	else:
		outobj = bpy.data.objects[outname]
	
	print("Tessellating...", outname, outobj);
	
	bm = bmesh.new()
	bm.from_object(ob, bpy.context.scene)
	#bm.from_mesh(ob.data)
	
	min1 = Vector([1e17, 1e17, 1e17])
	max1 = Vector([-1e17, -1e17, -1e17])
	
	mat = ob.matrix_world.copy()

	for v in bm.verts:
		v.co = mat * v.co

		for j in range(3):
			min1[j] = min(min1[j], v.co[j]);
			max1[j] = max(max1[j], v.co[j]);

	if min1[0] == 1e17:
		return
	
	#add a small margin
	d = 0.5
	min1 -= Vector([d, d, d]);
	max1 += Vector([d, d, d]);

	print("AABB", ob.name, min1, max1);
	#return
	mesh.surfmesh(outobj, min1=min1, max1=max1)

	from lg import appstate
	appstate.start_events()
