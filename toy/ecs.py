"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

from entities import ComponentDict, BaseEntity
from modifiers import BaseModifierType
from values import BaseValue
from processes import BaseProcess

def empty():
  pass

class System(dict):
  
  def __init__(self, **kwargs):
    self.default = dict(kwargs)
    self._processes = dict()
    self._process_queue = list()
    self.modtypes = dict()
    self.eid = 0
    self._running = False
    
    class Value(BaseValue):
      root = self

    class Entity(BaseEntity):
      root = self

    class ModType(BaseModifierType):
      root = self
    
    class Process(BaseProcess):
      root = self

    self.Value = Value
    self.Entity = Entity
    self.ModType = ModType
    self.Process = Process

    for key in kwargs:
      self[key] = ComponentDict()
  
  def register_process(self, process, domain=None, priority=0, startup=empty, 
                        setup=empty, teardown=empty, shutdown=empty):

    if not domain:
      domain = set()

    # add exception here for invalid domains? IE, domains with components that
    # don't exist?
    domain_dict = {k:v for k, v in self.items() if k in domain}
    self._processes[process] = {"domain":domain_dict, "startup":startup, 
                                "setup":setup, "teardown":teardown,
                                "shutdown":shutdown, "priority":priority}
    self._process_queue.append(process)
    self._process_queue.sort(key=lambda x: self._processes[x]["priority"])
  
  def register_modtype(self, modtype, name):
    self.modtypes[name] = modtype
  
  def step(self):
    if self._running is False:
      for process in self._process_queue:
        self._processes[process]["startup"]()
      self._running = True
    for process in self._process_queue:
      self._processes[process]["setup"]()
      domain = self._processes[process]["domain"]
      if domain:
        eids = list(set.intersection(*[set(s) for s in domain.values()]))
      else:
        eids = list()
      for eid in eids:
        process(self.Entity(eid))
      self._processes[process]["teardown"]()


  def quit(self):
    for process in self._process_queue:
      self._processes[process]["shutdown"]()
