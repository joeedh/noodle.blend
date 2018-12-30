from .config import *
from . import globals

sinknodes = set(INPUT_NODES + OUTPUT_NODES)

class NodeSorter:
  def __init__(self, tree=None):
    self.nodes = []
    
    if tree != None:
      self.load(tree)
    self.owner_node = None #for groups
  
  def load(self, tree):
    for n in tree.nodes:
      self.nodes.append(n)
      
  def sort(self):
    lst = []
    self.sortlist = lst
    tag = set()
    
    def nodeid(n):
      return self.nodes.index(n)
      
    def rec(n):
      if nodeid(n) in tag: return
      tag.add(nodeid(n))
      
      for i in n.inputs:
        for l in i.links:
          src = l.from_node
            
          if nodeid(src) not in tag:
            rec(src)
      
      lst.append(n)
      
    for n in self.nodes:
      if n.bl_idname in sinknodes:
        rec(n)
