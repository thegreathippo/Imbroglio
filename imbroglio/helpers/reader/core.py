from ecs import Components
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
abilities = "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"
components.set_components(0, *abilities)
mods = "str_bonus", "dex_bonus", "con_bonus", "int_bonus", "wis_bonus", "cha_bonus"
components.set_components(0, *mods)
components.set_components(0, "all_bonus")
print(components["strength"][0])
print(components["dexterity"][0])
print(components["constitution"][0])
print(components["intelligence"][0])
print(components["wisdom"][0])
print(components["charisma"][0])
print(components["str_bonus"][0])
print(components["dex_bonus"][0])
print(components["con_bonus"][0])
print(components["int_bonus"][0])
print(components["wis_bonus"][0])
print(components["cha_bonus"][0])
print(components["all_bonus"][0])
