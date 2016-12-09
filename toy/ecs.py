from entities import ComponentDict, BaseEntity
from modifiers import BaseModifierType
from values import BaseValue

def empty():
  pass

class System(dict):
  
  def __init__(self, **kwargs):
    self.default = dict(kwargs)
    self._processes = dict()
    self._process_queue = list()
    self._modtypes = dict()
    self.eid = 0
    
    class Value(BaseValue):
      root = self

    class Entity(BaseEntity):
      root = self

    class ModType(BaseModifierType):
      root = self

    self.Value = Value
    self.Entity = Entity
    self.ModType = ModType

    for key in kwargs:
      self[key] = ComponentDict()
  
  def register_process(self, process, domain=None, priority=0, startup=empty, 
                        setup=empty, teardown=empty, shutdown=empty):

    if not domain:
      domain = set()

    self._processes[process] = {"domain":domain, "startup":startup, 
                                "setup":setup, "teardown":teardown,
                                "shutdown":shutdown, "priority":priority}
    self._process_queue.append(process)
    self._process_queue.sort(key=lambda x: self._processes[x]["priority"])
  
  def register_modtype(self, modtype, name):
    self._modtypes[name] = modtype
