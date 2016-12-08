from entities import BaseEntity

def empty():
  pass

class System(dict):
  
  def __init__(self, **kwargs):
    self.default = dict(kwargs)
    self._processes = dict()
    self._process_queue = list()
    self.eid = 0
    
    class Entity(BaseEntity):
      root = self

    self.Entity = Entity

    for key in kwargs:
      self[key] = dict()
  
  def register_process(self, process, domain=None, priority=0, startup=empty, 
                        setup=empty, teardown=empty, shutdown=empty):

    if not domain:
      domain = set()

    self._processes[process] = {"domain":domain, "startup":startup, 
                                "setup":setup, "teardown":teardown,
                                "shutdown":shutdown, "priority":priority}
    self._process_queue.append(process)
    self._process_queue.sort(key=lambda x: self._processes[x]["priority"])

