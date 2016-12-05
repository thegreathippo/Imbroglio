"""
Core module for Imbroglio's ecs (Entity Component architecture). Based 
loosely on JAForbes' idea: 

https://gist.github.com/JAForbes/99c15c0995b87a22b95a

This module provides access to the Components class; a custom Python 
dict. Instances of this class can be used to generate new components, 
assign them (and their values) to entities, register new processes, and 
add (or remove) modifiers to an entity's component.

Samples:

>>> player = 1
>>> component = Components(x=1, y=2)
>>> component.set_components(player, "x", "y")
>>> component["x"][player]
> 1
>>> component["y"][player]
> 2


TODO:
  * Change 'Aspect' class to 'Process'.
  * Make 'add_aspect' into 'register_process'; set it up so it can take 
    arbitrary functions with kwargs (and the Process instancing just does 
    this automatically for you).
  * Change 'run' (in Process classes) to '__call__'
  * Move '_get_uids' to Components? Just performs a set intersection on
    a group of given components? 
  * 'setup', etc -- these methods are accessed via Components in a try
    except block.
  * More precise error handling.
    * Specifically: Components.remove_components should tell us which 
      components did not contain the given uid.
  * Should be a way to create entities via aspects rather than via 
    components.
  * Entities should also be removable via aspects.
  * Update documentation to reflect move from parser at top-level top-level
    to bottom-level (modifiers)
"""
from aspects import BaseAspect
from entities import BaseEntities, BaseEntity


class Components(dict):
  """Class for Components instances.
  
  Inherits from Python 3.x's dict class, while providing some additional
  functionality.
  
  Attributes:
    Aspect: The Components instance's Aspect class. This class is defined 
      within Components.__init__; therefore, it is unique to each instance 
      of Components. Classes which inherit from a Components instance's 
      Aspect class will be automatically instanced and handled internally 
      by the Components instance. 
    
      For more information, see the aspects.py module.
  """

  def __init__(self, **kwargs):
    """Create an instance of Components.
    
    Args:
      **kwargs: Component names and the default values associated with 
        those components.
    """
    
    self._default = dict(kwargs)

    class Aspect(BaseAspect):
      root = self
    
    class Entity(BaseEntity):
      root = self

    class Entities(BaseEntities):
      root = self
    
    super().__init__()
    self._aspects = list()
    self.modifiers = dict()
    for key in kwargs:
      self[key] = Entities(key)
    self.Aspect = Aspect
    self.Entity = Entity

  def add_aspect(self, cls):
    """Instance a class and add it as an aspect to the Components 
    instance.
    Note:
      Unless you know what you're doing, you shouldn't call this method; 
      it's primarily for internal use by Components itself.
    Args:
      cls: The class to be instanced and added to Components._aspects. 
        Classes used for this purpose should have a process method (one 
        that requires no arguments), and a priority class attribute
        (that can be sorted).
    
    Returns:
      None
    """
    self._aspects.append(cls())
    self._aspects.sort(key=lambda x: x.priority)
  
  def run(self):
    """Run each of the Component instance's aspects (processes) once, 
    in order.
    
    Returns:
      None
    """
    for aspect in self._aspects:
      aspect.process()

  def set_components(self, uid, *args, **kwargs):
    """Set the values of one or more components for an entity.
    Note:
      Any component set as a string enclosed in OPEN_FORMULA and
      CLOSE_FORMULA will be treated as a formula. The string will be 
      evaluated and replaced with a function, which will be called 
      whenever this component's value is retrieved.
      
      For more information, see the parser.core.py module.
    Args:
      uid (any hashable value): The entity for which these components 
        will be defined.
      *args: Components (strings); these components will be set to their
        default values for the entity. Raises an exception if any of 
        these values are not in the Components instance.
      **kwargs: Components to values; these components will be set to 
        the given value for the entity. Raises an exception if any of 
        kwargs' keys are not in the Components instance.
    Returns:
      None
    """
    if not set(args).issubset(self) or not set(kwargs).issubset(self):
      invalid = set(kwargs).difference(self).union(set(args).difference(self))
      # Write better exception later
      raise Exception("Cannot set {}; not components".format(invalid))
    for comp_name in set(args).union(kwargs):
      value = kwargs.get(comp_name, self._default[comp_name])
      self[comp_name][uid] = value

  def remove_components(self, uid, *args):
    """Remove one or more components from a given entity.
    
    Args:
      uid (any hasable value): The entity for which these components 
        will be removed.
      *args: Components (strings); these components will remove the 
        given entity from themselves. Raises an exception if any of 
        these strings are not in the Components instance; also raises 
        an exception if uid is not associated with any of these 
        components.
    Returns:
      None
    """
    for arg in args:
      try:
        self[arg]
      except KeyError:
        # Write better exception later
        raise Exception("Cannot delete {}; not a component".format(arg))
      try:
        del self[arg][uid]
      except KeyError:
        # Write better exception later
        raise Exception("Cannot delete {}; entity doesn't exist".format(uid))
