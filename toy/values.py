from parser import Parser

OPEN, CLOSE = "{", "}"

class BaseValue:
  root = None

  def __init__(self, eid, value):
    self._eid = eid
    self._modifiers = dict()
    self.base = value

  @property
  def base(self):
    return self._base
  
  @base.setter
  def base(self, value):
    self._base = self._parse(self._eid, value)
  
  def _parse(self, entity, value):
    ret_value = value
    try:
      if value.startswith(OPEN) and value.endswith(CLOSE):
        entity = self.root.Entity(self._eid)
        parser = Parser(entity=entity)
        ret_value = parser(value[1:-1])
    except AttributeError:
      pass
    return ret_value

  def __call__(self):
    value = self.base
    if callable(value):
      value = value()
    for mod in self._modifiers.values():
      value = mod.modify(value)
    return value
  
  def __getattr__(self, attr):
    if attr in self._modifiers:
      return self._modifiers[attr]
    else:
      if attr in self.root._modtypes:
        modifier = self.root._modtypes[attr]()
        self._modifiers[attr] = modifier
        return modifier
    super().__getattribute__(attr)


