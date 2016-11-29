#toy code
player = 1
monster = 2
wall = 3


class Components:
  
  def __init__(self, *components):
    self.__dict__.update({k:{} for k in components})

  def add_aspect(self, name, *components):
    self.__dict__[name] = Aspect(**{c:self.__dict__[c] for c in components})


class Aspect:
  
  def __init__(self, **components):
    self._components = components.values()
    self._views = []
    for d in components.values():
      self._views.append(d.keys())
    super().__init__()

  def get_uids(self):
    return set.intersection(*[set(s) for s in self._views])

  def clear_uid(self, uid):
    for d in self._components:
      if uid in d:
        del d[uid]


components = Components("x", "y", "vx", "vy")
components.x[player], components.y[player] = 0, 0
components.vx[player], components.vy[player] = 0, 0
components.x[monster], components.y[monster] = 0, 0
components.vx[monster], components.vy[monster] = 0, 0
components.x[wall], components.y[wall] = 0, 0


components.add_aspect("Physics", "x", "y", "vx", "vy")  

print(components.Physics.get_uids())
components.Physics.clear_uid(player)
print(components.Physics.get_uids())
