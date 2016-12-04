# Entity-Component architecture based loosely on JAForbes' idea:
# https://gist.github.com/JAForbes/99c15c0995b87a22b95a
from parser import Parser


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
    self.startup()

  def startup(self):
    pass

  def setup(self):
    pass
  
  def process(self):
    self.setup()
    for uid in self._get_uids():
      self.run(uid)
    self.teardown()

  def run(self, uid):
    pass

  def teardown(self):
    pass

  def _get_uids(self):
    if self:
      return list(set.intersection(*[set(s) for s in self.values()]))
    return list()

  def __repr__(self):
    return self.__class__.__name__ + " " + super().__repr__()

  
class Components(dict):

  def __init__(self, **kwargs):
    self._default = dict(kwargs)
    class Aspect(BaseAspect):
      root = self
    
    super().__init__()
    self._aspects = list()
    for key in kwargs:
      self[key] = _Entities()
    self.Aspect = Aspect


  def add_aspect(self, cls):
    self._aspects.append(cls())
    self._aspects.sort(key=lambda x: x.priority)
  
  def run(self):
    for aspect in self._aspects:
      aspect.process()

  def set_components(self, uid, *args, **kwargs):
    for arg in args:
      try:
        value = self._default[arg]
      except KeyError:
        # Write better exception later
        raise Exception("Cannot set {}; not a component".format(arg))
      try:
        if value.startswith("{") and value.endswith("}"):
          parser = Parser(component=self, entity=uid)
          self[arg][uid] = parser(value[1:-1])
      except AttributeError:
        self[arg][uid] = value
    for key in kwargs:
      try:
        self[key]
      except KeyError:
        # Write better exception later
        raise Exception("Cannot assign {0} to {1}; not a component".format(key, kwargs[key]))
      value = kwargs[key]
      try:
        if value.startswith("{") and value.endswith("}"):
          parser = Parser(component=self, entity=uid)
          self[key][uid] = parser(value[1:-1])
      except AttributeError:
        self[key][uid] = value

  def remove_components(self, uid, *args):
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


class _Entities(dict):

  def __getitem__(self, key):
    item = super().__getitem__(key)
    if callable(item):
      return item()
    return item
