#toy code
player = 1
monster = 2
wall = 3

x = {player: 5, monster:4, wall: 4}
y = {player: 6, monster:3, wall: 6}
vx = {player: 0, monster:0}
vy = {player: 0, monster:0}



class Domain(dict):
  
  def __init__(self, *components):
    self._views = []
    for component in components:
      self._views.append(component.keys())
    super().__init__()

  def get_entities(self):
    return set.intersection(*[set(s) for s in self._views])
  
  
d = Domain(x, y, vx, vy)

print(d.get_entities())
