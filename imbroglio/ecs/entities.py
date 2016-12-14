"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

class ComponentDict(dict):
  def __getitem__(self, key):
    if hasattr(key, "get_eid"):
      key = key.get_eid()
    return super().__getitem__(key)


class BaseEntity:
  root = None

  def __init__(self, _eid=None, **kwargs):
    if _eid is None:
      eid = self.root.eid
      self.root.eid += 1
    else:
      if hasattr(_eid, "get_eid"):
        _eid = _eid.get_eid()
      eid = _eid
    super().__setattr__("_eid", eid)
    for key in kwargs:
      if kwargs[key] is None:
        default = self.root.default[key]
        # if this is a class, like dict, or
        # list, or a custom class, then instance it
        if (isinstance(default, type)):
          default = default()
        setattr(self, key, default)
      else:
        setattr(self, key, kwargs[key])

  def get_eid(self):
    return self._eid

  def __getattr__(self, attr):
    try:
      value = self.root[attr][self._eid]
    except KeyError:
      super().__getattribute__(attr)
    if callable(value):
      return value()
    return value

  def __setattr__(self, attr, value):
    if attr not in self.root:
      #better exception later
      raise Exception("System does not have {}".format(attr))
    if self._eid in self.root[attr]:
      self.root[attr][self._eid].base = value
    else:
      self.root[attr][self._eid] = self.root.Value(self._eid, value)

  def __delattr__(self, attr):
    del self.root[attr][self._eid]
  
  def __getitem__(self, key):
    return self.root[key][self._eid]

