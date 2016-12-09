from .ecs import Components
import re

def load_components(path):
  data = dict()
  with open(path, "r") as file:
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
      data[key] = val
  return Components(**data)
