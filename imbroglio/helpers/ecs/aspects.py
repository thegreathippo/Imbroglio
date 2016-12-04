"""Aspect module for Imbroglio's ecs (Entity Component architecture).

This module provides access to the BaseAspect class, which inherits from
Python 3.x's dict class. BaseAspect is imported by ecs.core.py, where it 
is included as an attribute in instances of the Components class.

TODO:
  * Better (more descriptive) exceptions.
  * Better terminology (swap out uids for entities?).
"""

class _AspectType(type):
  """Metaclass for Aspects.
  
  Note:
    This is private for a reason; you shouldn't be mucking about with 
    this. Its only real purpose is to serve as a hook so that instances 
    of Components can instance the children of BaseAspect automatically.
  """

  def __new__(cls, name, bases, namespace):
    new_cls = super().__new__(cls, name, bases, namespace)
    if new_cls.root:
      new_cls.root.add_aspect(new_cls)
    return new_cls


class BaseAspect(dict, metaclass=_AspectType):
  """Base class for Aspects.

  Inherits from Python 3.x's dict class, while providing some additional
  functionality.
  
  Class Attributes:
    domain: A set of components (strings) which this Aspect governs; 
      these are the components an entity must be associated with in 
      order to be processed by this Aspect.
    priority: This value determines the order in which this aspect will 
      run its code in relation to other aspects. The lower this number 
      is, the closer to the front this aspect will be.
    root: This is the Components instance responsible for instancing 
      this Aspect.
  """

  domain = {}
  priority = 0
  root = None

  def __init__(self):
    """Create an instance of BaseAspect."""
    super().__init__()
    self.update({k:v for k, v in self.root.items() if k in self.domain})
    if not set(self.domain).issubset(self.root.keys()):
      # write a more descriptive exception later
      raise Exception("{0} instanced with invalid domain ({1})".format(self, self.domain))
    self.startup()

  def startup(self):
    """A hook that runs after the Aspect instance is initialized."""
    pass

  def setup(self):
    """A hook that runs before the Aspect begins processing entities."""
    pass
  
  def process(self):
    """Process the Aspect, activating its setup, run, and teardown 
    hooks.
    """
    self.setup()
    for uid in self._get_uids():
      self.run(uid)
    self.teardown()

  def run(self, uid):
    """Process a single entity that intersects with this Aspect 
    instance's domain (it is associated with all the components in the 
    Aspect's domain).
    """
    pass

  def teardown(self):
    """A hook that runs after the Aspect finishes processing entites."""

  def _get_uids(self):
    if self:
      return list(set.intersection(*[set(s) for s in self.values()]))
    return list()

  def __repr__(self):
    return self.__class__.__name__ + " " + super().__repr__()

