"""
Core module for imbroglio's entity-component system. Based loosely on 
JAForbes' idea:

https://gist.github.com/JAForbes/99c15c0995b87a22b95a

This module provides access to the System class, a custom Python dict that 
is responsible for storing all component-to-entity relationships, while also 
allowing for registration of processes to act on those entities (and modifiers 
to temporarily modify those values).

Example:
  >>> from ecs import System
  >>> world = System(x=0, y=0)
  >>> player = world.Entity(x=None, y=None)
  >>> player.x
  > 0
  >>> def move_x(entity):
  >>>   entity.x += 1
  >>> world.register_process(move_x, domain={"x", "y"})
  >>> world.step()
  >>> player.x
  > 1

TODO:
  * More precise error handling.
  * Method to destroy entities? 
"""

from .entities import ComponentDict, BaseEntity
from .values import BaseValue
from .processes import BaseProcess

def _empty():
  pass

class System(dict):
  """Class for System instance.

  Inherits from Python's dict class, while adding additional functionality.
  
  Attributes:
    default (dict): Components to values. These are used in cases when a 
      component's value is set to None.
    Entity (class): The Entity class used to instance entities from the System 
      instance. Entity classes do not actually contain component data; they 
      merely provide a handle to access this data through the System instance.
      For more information, see entities.py.
    eid (int): A counter used to produce unique identities for Entities 
      instanced with no defined identity.
    Process (class): Any class which inherits from this class will be 
      automatically instanced and registered as a process for this System 
      instance. Provided as an alternative to manually registering processes 
      (via System.register_process).
    Value (class): Wraps component values (which allows for parsing and
      modifiers). For more information, see values.py.
    running (boolean): True if the system is currently running; False if 
      it is not.
  """
  
  def __init__(self, **kwargs):
    """Create an instance of System.

    Args:
      **kwargs: Components and their default values. Values cannot be None.
    """
    self.default = dict(kwargs)
    self._processes = dict()
    self._process_queue = list()
    self.eid = 0
    self.running = False

    class Value(BaseValue):
      root = self

    class Entity(BaseEntity):
      root = self

    class Process(BaseProcess):
      root = self

    self.Value = Value
    self.Entity = Entity
    self.Process = Process

    for key in kwargs:
      self[key] = ComponentDict()

  def register_process(self, process, domain=None, priority=0, startup=_empty, 
                        setup=_empty, teardown=_empty, shutdown=_empty):
    """Register a process within this System instance.

    Args:
      process (callable): An object that accepts a single argument (an entity).
      domain (container, optional): A group of components that an entity must 
        have for the process to act upon it. 
      priority (int, optional): The order in which this process will be 
        executed (lower is sooner; 0 executes before 1). Defaults to 0.
      startup (callable, optional): An object that can be called without 
        arguments; called when the System instance first begins to run. 
        Defaults to an empty function.
      setup (callable, optional): An object that can be called without 
        arguments; called before the process object begins accepting 
        entities. Defaults to an empty function.
      teardown (callable, optional): An object that can be called without 
        arguments; called whenever the process object has iterated through all 
        relevant entities. Defaults to an empty function.
      shutdown (callable, optional): An object that can be called without 
        arguments; called whenever the System instance is shutting down, 
        Defaults to an empty function.
    """
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
  
  def step(self):
    """Take a single step within the System instance, executing all relevant 
    processes and their hooks.
    """
    if self.running is False:
      for process in self._process_queue:
        self._processes[process]["startup"]()
      self.running = True
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
    """Close all processes in the System instance, executing their shutdown 
    hooks.
    """
    self.running = False
    for process in self._process_queue:
      self._processes[process]["shutdown"]()
