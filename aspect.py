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

  def remove_uid(self, uid):
    for d in self.__dict__.values():
      if uid in d:
        del d[uid]

  def run_process(self, process):
    for uid in self.get_uids():
      process(self, uid)


def move_things(physics, uid):
  physics.x[uid] += physics.vx[uid]
  physics.y[uid] += physics.vy[uid]


components = Components("x", "y", "vx", "vy")
components.x[player], components.y[player] = 0, 0
components.vx[player], components.vy[player] = 1, 1
components.x[monster], components.y[monster] = 0, 0
components.vx[monster], components.vy[monster] = -1, -1
components.x[wall], components.y[wall] = 0, 0


components.add_aspect("Physics", "x", "y", "vx", "vy")  
components.add_aspect("Position", "x", "y")

print(components.Physics.__dict__)
components.Physics.run_process(move_things)
print(components.Physics.__dict__)
del components.vy[player]
components.Physics.run_process(move_things)
print(components.Physics.__dict__)
