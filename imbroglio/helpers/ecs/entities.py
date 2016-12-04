class Entities(dict):

  def __getitem__(self, key):
    item = super().__getitem__(key)
    if callable(item):
      return item()
    return item


class EntityHandler:
  def __init__(self, uid, _dict):
    self._uid = uid
    self._dict = _dict

  def __getattr__(self, attr):
    return self._dict[attr][self._uid]

