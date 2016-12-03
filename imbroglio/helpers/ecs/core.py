# Entity-Component architecture based loosely on JAForbes' idea:
# https://gist.github.com/JAForbes/99c15c0995b87a22b95a

world = 0
player = 1
monster = 2


class AspectType(type):
  """Metaclass for Aspects."""

  def __new__(cls, name, bases, namespace):
    new_cls = super().__new__(cls, name, bases, namespace)
    if new_cls.root:
      new_cls.root.add_aspect(new_cls)
    return new_cls


class BaseAspect(dict, metaclass=AspectType):
  """Base class for Aspects."""
  domain = {}
  priority = 0
  root = None

  def __init__(self):
    super().__init__()
    self.update({k:v for k, v in self.root.items() if k in self.domain})
    if not set(self.domain).issubset(self.root.keys()):
      # write a more descriptive exception later
      raise Exception("{0} instanced with invalid domain ({1})".format(self, self.domain))

  def setup(self):
    pass
  
  def process(self):
    self.setup()
    for uid in self._get_uids():
      self.run(uid)
    self.teardown()

  def run(self, uid):
    print(str(self) + ": " + str(uid))

  def teardown(self):
    pass

  def _get_uids(self):
    if self:
      return list(set.intersection(*[set(s) for s in self.values()]))
    return list()

  def __repr__(self):
    return self.__class__.__name__ + " " + super().__repr__()

  
class Components(dict):

  def __init__(self, *args):
    class Aspect(BaseAspect):
      root = self
    
    super().__init__()
    self._aspects = list()
    for arg in args:
      self[arg] = _Entities()
    self.Aspect = Aspect


  def add_aspect(self, cls):
    self._aspects.append(cls())
    self._aspects.sort(key=lambda x: x.priority)
  
  def run(self):
    for aspect in self._aspects:
      aspect.process()

class _Entities(dict):

  def __getitem__(self, key):
    item = super().__getitem__(key)
    if callable(item):
      return item()
    return item

component = Components("x", "y")
component["x"][player] = 1
component["y"][player] = 2
component["x"][monster] = 0
component["y"][monster] = 4


class Physics(component.Aspect):
  domain = {"x", "y"}


class Physics2(component.Aspect):
  domain = {"x", "y"}
  priority = -1


component.run()
