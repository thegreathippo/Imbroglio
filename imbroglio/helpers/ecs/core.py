# Entity-Component architecture based loosely on JAForbes' idea:
# https://gist.github.com/JAForbes/99c15c0995b87a22b95a
from aspects import BaseAspect
from entities import Entities, EntityHandler
from .parser import Parser

OPEN_FORMULA, CLOSE_FORMULA = "{", "}"


class Components(dict):

  def __init__(self, **kwargs):
    self._default = dict(kwargs)

    class Aspect(BaseAspect):
      root = self

    super().__init__()
    self._aspects = list()
    for key in kwargs:
      self[key] = Entities()
    self.Aspect = Aspect

  def add_aspect(self, cls):
    self._aspects.append(cls())
    self._aspects.sort(key=lambda x: x.priority)
  
  def run(self):
    for aspect in self._aspects:
      aspect.process()

  def set_components(self, uid, *args, **kwargs):
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

