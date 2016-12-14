"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
import parser as parse
from modifiers import Modifiers
Parser = parse.Parser

OPEN, CLOSE = "{", "}"

class BaseValue:
  root = None

  def __init__(self, eid, value):
    self._eid = eid
    self._swap_mods = list()
    self.modifiers = Modifiers(self)
    self.raw = value
    self.base = value

  @property
  def base(self):
    return self._base
  
  @base.setter
  def base(self, value):
    self._base = self.parse(value)
  
  def parse(self, value):
    ret_value = value
    try:
      if value.startswith(OPEN) and value.endswith(CLOSE):
        entity = self.root.Entity(self._eid)
        parser = Parser(entity=entity)
        ret_value = parser(value[1:-1])
    except AttributeError:
      pass
    return ret_value

  def add(self, value, source=None, *tags):
    def _add(val, modval):
      if callable(modval):
        modval = modval()
      return val + modval
    return self.modifiers(value, _add, source, *tags)
  
  def swap(self, value, source=None, *tags):
    def _swap(val, modval):
      if callable(modval):
        modval = modval()
      return modval
    return self.modifiers(value, _swap, source, *tags)

  def __call__(self):
    value = self.base
    if callable(value):
      try:
        value = value()
      except parse.InvalidInternalError as e:
        if e.raw.split(".")[1] in self.root:
          return None
        raise e
    value = self.modifiers.modify(value)
    return value
  


