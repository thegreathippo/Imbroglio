#toy code
player = 1
monster = 2
wall = 3


class Components:
  
  def __init__(self, *components):
    self.__dict__.update({k:{} for k in components})
    self._processes = []

  def add_aspect(self, name, *components):
    self.__dict__[name] = Aspect(**{c:self.__dict__[c] for c in components})


class Aspect:
  
  def __init__(self, **components):
    self.__dict__.update(components)

  def get_uids(self):
    return list(set.intersection(*[set(s) for s in self.__dict__.values()]))

  def clear_uid(self, uid):
    for d in self.__dict__.values():
      if uid in d:
        del d[uid]




components = Components("x", "y", "vx", "vy")
components.x[player], components.y[player] = 0, 0
components.vx[player], components.vy[player] = 0, 0
components.x[monster], components.y[monster] = 0, 0
components.vx[monster], components.vy[monster] = 0, 0
components.x[wall], components.y[wall] = 0, 0


components.add_aspect("Physics", "x", "y", "vx", "vy")  
components.add_aspect("Position", "x", "y")


print("Physics: " + str(components.Physics.get_uids()))
print("Position: " + str(components.Position.get_uids()))
print("Removing vx from Player")
del components.vx[player]
print("Physics: " + str(components.Physics.get_uids()))
print("Position: " + str(components.Position.get_uids()))
print("Removing everything from Player")
components.Physics.clear_uid(player)
print("Physics: " + str(components.Physics.get_uids()))
print("Position: " + str(components.Position.get_uids()))
components.x[player]=1
components.y[player]=0
components.vx[player]=0
components.vy[player]=0
print("Physics: " + str(components.Physics.get_uids()))
print("Position: " + str(components.Position.get_uids()))


