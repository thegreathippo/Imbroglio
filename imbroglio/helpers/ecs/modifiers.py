from .parser import Parser

OPEN, CLOSE = "{", "}"

class Modifiers:
  def __init__(self, key, value, root):
    try:
      if value.startswith(OPEN) and value.endswith(CLOSE):
        handler = root.Entity(key)
        parser = Parser(component=self, entity=handler)
        self._value = parser(value[1:-1])
      else:
        self._value = value
    except AttributeError:
      self._value = value
    self._root = root
    self._mods = list()

  def __call__(self):
    value = self._value
    if callable(self._value):
      value = self._value()
    for mod in self._mods:
      value = mod(value)
    return value

  def add_modifier(self, modifier):
    self._mods.append(modifier)



