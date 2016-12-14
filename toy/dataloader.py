import collections

nt = collections.namedtuple
OrderedDict = collections.OrderedDict

terms = {
  "COMPONENT": nt("Component", ["name", "default"]),
  "TEMPLATE": nt("Template", ["name"])
  }

def build_tree(path):
  with open(path, "r") as f:
    tree = dict()
    for k in terms:
      tree[k] = OrderedDict()
    node = None
    for line in f:
      line=line.rstrip()
      x = len(line)
      line=line.lstrip()
      if not line:
        continue
      indent = x - len(line)
      data = _trim_args(line)
      term = data[0]
      if indent == 0:
        if term not in terms:
          raise Exception("Illegal term: {}".format(term))
        new_list = list()
        r = terms[term](*data[1:])
        tree[term][r] = new_list
        node = new_list
      else:
        try:
          node.append(data)
        except AttributeError:
          raise Exception("Invalid file: {}".format(path))
  return tree

def _trim_args(line):
  ret_list = list()
  trimmed = line[1:-1].split(":")
  for s in trimmed:
    ret_list.append(s.rstrip().lstrip())
  return ret_list

def get_constructors(path):
  data_tree = build_tree(path)
  comp_cons = ComponentConstructor(data_tree["COMPONENT"])
  temp_cons = TemplateConstructor(data_tree["TEMPLATE"])
  return comp_cons, temp_cons
  
class ComponentConstructor(dict):
  def __init__(self, data):
    super().__init__()
    for c in data:
      default = _refine_value(c.default)
      self[c.name] = default


class TemplateConstructor(dict):
  def __init__(self, data):
    super().__init__()
    for t in data:
      self[t.name] = dict()
      for line in data[t]:
        term, value = line[0], line[1]
        if term == "INCLUDE":
          self[t.name].update(self[value])
        if term == "DEFAULT":
          self[t.name][value] = None
        elif term == "SET":
          val = _refine_value(line[2])
          self[t.name][value] = val


def _refine_value(value):
  try:
    ret_val = int(value)
  except ValueError:
    if value == "list":
      ret_val = list
    elif value == "dict":
      ret_val = dict
    elif value == "set":
      ret_val = set
    elif value == "None":
      ret_val = None
    else:
      ret_val = value
  return ret_val
