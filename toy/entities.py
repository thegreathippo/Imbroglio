class ComponentDict(dict):
  def __getitem__(self, key):
    if hasattr(key, "get_eid"):
      key = key.get_eid()
    return super().__getitem__(key)


class BaseEntity:
  root = None

  def __init__(self, *args, **kwargs):
    if not args:
      eid = self.root.eid
      self.root.eid += 1
    else:
      eid = args[0]
    super().__setattr__("_eid", eid)
    for key in kwargs:
      if kwargs[key] is None:
        setattr(self, key, self.root.default[key])
      else:
        setattr(self, key, kwargs[key])

  def get_eid(self):
    return self._eid

  def __getattr__(self, attr):
    value = self.root[attr][self._eid]
    if callable(value):
      return value()
    return value

  def __setattr__(self, attr, value):
    if self._eid in self.root[attr]:
      self.root[attr][self._eid].base = value
    else:
      self.root[attr][self._eid] = self.root.Value(self._eid, value)

  def __delattr__(self, attr):
    del self.root[attr][self._eid]
  
  def __getitem__(self, key):
    return self.root[key][self._eid]

