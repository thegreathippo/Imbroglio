from modifiers import Modifiers

class BaseEntity:
  root = None

  def __init__(self, eid=None, **kwargs):
    if eid is None:
      eid = self.root.eid
      self.root.eid += 1
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
    self.root[attr][self._eid] = Modifiers(self, value)

