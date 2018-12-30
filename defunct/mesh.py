from . import c_code, symbol;
from math import *
import bmesh
from mathutils import *

from ctypes import *

def fract(f):
  return f - floor(f)

def perlin(x, y, z):
  return 0.0;

def perlin_dv(x, y, z, dx, dy, dz):
  return 0.0;
  
def surfmesh(outobj, outmatrix=None, min1=None, max1=None):
  if outmatrix is None:
    outmatrix = Matrix()
    outmatrix.resize_4x4()
    
  if min1 == None: min1 = Vector([-1, -1, -1])
  if max1 == None: max1 = Vector([1, 1, 1])
  
  #"""
  rs = [
    Vector([min1[0], min1[1], min1[2]]),
    Vector([min1[0], max1[1], min1[2]]),
    Vector([max1[0], max1[1], min1[2]]),
    Vector([max1[0], min1[1], min1[2]]),
    Vector([min1[0], min1[1], max1[2]]),
    Vector([min1[0], max1[1], max1[2]]),
    Vector([max1[0], max1[1], max1[2]]),
    Vector([max1[0], min1[1], max1[2]]),
  ]
  
  #identity matrix
  mat = (c_float*16)()
  for i in range(4):
    for j in range(4):
      mat[j*4+i] = 0.0

  for i in range(4):
    mat[i*4+i] = 1
        
  _min = (c_float*3)()
  _max = (c_float*3)()
  
  for i in range(3):
    _min[i] = min1[i]
    _max[i] = max1[i]

  min1 = _min; max1 = _max;
  
  verts = POINTER(c_float)();
  ao_out = POINTER(c_float)();
  totvert = c_int(0);
  tris = POINTER(c_int)()
  tottri = c_int(0)
  
  from . import scene
  sg = scene.thescene

  c_code._lib.sm_tessellate(c_voidp(sg.handle), byref(verts), byref(ao_out), byref(totvert), byref(tris), byref(tottri), 
                     min1, max1, c_int(6), mat, c_int(0));
  
  #return#XXX
  
  print("\n\n")
  print("finished tessellating; totvert:", totvert.value, "tottri:", tottri.value)
  print("\n")
  print(verts, tris)

  bm = bmesh.new()
  vs = []
  for i in range(totvert.value):
    co = Vector([verts[i*3], verts[i*3+1], verts[i*3+2]])
    
    v = bm.verts.new(co)
    vs.append(v)
  
  bm.verts.index_update()
  
  vlen = len(bm.verts)
  for i in range(tottri.value):
    #print(tris[i*3+2], len(bm.verts))
    v1 = tris[i*3]
    v2 = tris[i*3+1]
    v3 = tris[i*3+2]
    
    if (v3 >= vlen or v2 >= vlen or v1 >= vlen):
      print("BAD TRI!")
      continue;
      
    if v1 == v2 or v2 == v3 or v1 == v3:
      continue
      
    v1 = vs[v1]; v2 = vs[v2]; v3 = vs[v3]
    #print(v1, v2, v3)
    try:
      f = bm.faces.new([v1, v2, v3])
      f.smooth = True
    except ValueError:
      pass
  
  c_code._lib.sm_free_tess(verts, tris);
  
  bm.to_mesh(outobj.data)
  outobj.data.update()
    
    
    