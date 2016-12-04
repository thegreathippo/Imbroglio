"""Core module for Imbroglio's ecs (Entity Component architecture).

Based loosely on JAForbes' idea: 
https://gist.github.com/JAForbes/99c15c0995b87a22b95a

This module provides access to the Components class, which inherits from
Python 3.x's dict class. Instances of this class can be used to generate
new components, assign them (and their values) to entities, instance 
Aspect classes (automatically via inheritance), and run the process 
method of Aspect instances.

Attributes:
	OPEN_FORMULA (str): When setting string values to an entity's 
	  component, any string which begins with this value (and 
		ends with CLOSE_FORMULA) will be treated as a formula.

	CLOSE_FORMULA (str): When setting string values to an entity's
	  component, any string which ends with this value (and 
		begins with OPEN_FORMULA) will be treated as a formula.

TODO:
  * More precise error handling.
    * Specifically: Components.remove_components should tell us which 
      components did not contain the given uid.
  * Clean up terminology.
    * Entities/uids shouldn't be interchangeable; pick one (prolly 
      entities).
	* Templating system (?)
	* A type of domain that auto-cycles through all entities (?)
	* Should be a way to create entities via aspects rather than via 
	  components.
	* Entities should also be removable via aspects.
"""
from aspects import BaseAspect
from entities import Entities, EntityHandler
from parser import Parser

OPEN_FORMULA, CLOSE_FORMULA = "{", "}"


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

    super().__init__()
    self._aspects = list()
    for key in kwargs:
      self[key] = Entities()
    self.Aspect = Aspect

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
    """
    if not set(args).issubset(self) or not set(kwargs).issubset(self):
      invalid = set(kwargs).difference(self).union(set(args).difference(self))
      # Write better exception later
      raise Exception("Cannot set {}; not components".format(invalid))
    for comp_name in set(args).union(kwargs):
      value = kwargs.get(comp_name, self._default[comp_name])
      try:
        if value.startswith(OPEN_FORMULA) and value.endswith(CLOSE_FORMULA):
          handler = EntityHandler(uid, self)
          parser = Parser(component=self, entity=handler)
          self[comp_name][uid] = parser(value[1:-1])
      except AttributeError:
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
