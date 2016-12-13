"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
from .parser import Parser

OPEN, CLOSE = "{", "}"

class BaseValue:
  root = None

  def __init__(self, eid, value):
    self._eid = eid
    self._add_mods = list()
    self._swap_mods = list()
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

  def __call__(self, target=None):
    value = self.base
    if callable(value):
      value = value()
    for mod in self._swap_mods:
      if callable(mod.value):
        value = mod.value()
      else:
        value = mod.value
    for mod in self._add_mods:
      if callable(mod.value):
        value += mod.value()
      else:
        value += mod.value
    return value
  
  def add(self, value, source=None, tags=None):
    mod = Modifier(self, value, source, tags)
    self._add_mods.append(mod)
    return mod

  def swap(self, value, source=None, tags=None):
    mod = Modifier(self, value, source, tags)
    self._swap_mods.append(mod)
    return mod
  
  def remove(self, mod):
    try:
      self._add_mods.remove(mod)
    except ValueError:
      pass
    try:
      self._swap_mods.remove(mod)
    except ValueError:
      pass


class Modifier:
  def __init__(self, owner, mod_value, source, tags):
    if tags is None:
      tags = list()
    self._owner = owner
    self.source = source
    self.tags = tags
    self.value = owner.parse(mod_value)

  def remove(self):
    self._owner.remove(self)



