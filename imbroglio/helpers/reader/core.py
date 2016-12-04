from .ecs import Components
import re

def load_components(path):
  components = dict()
  file = open(path, "r")
  for line in file.readlines():
    if re.match(r'\n', line): # new line
      continue
    comp_to_val = line.replace(" ", "").replace("\n", "").split("=")
    if len(comp_to_val) != 2:
      continue
    key, val = comp_to_val
    try:
      val = int(val)
    except ValueError:
      pass
    components[key] = val
  return components

data = load_components("components.dat")
components = Components(**data)
components.set_components(0, "str_bonus", "strength")
print(components["str_bonus"][0])
