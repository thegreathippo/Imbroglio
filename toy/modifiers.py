class _BaseModTypeType(type):
  def __new__(cls, name, bases, namespace):
    new_cls = super().__new__(cls, name, bases, namespace)
    if new_cls.root:
      new_cls.root.register_modtype(new_cls, name)
    return new_cls


class BaseModifierType(metaclass=_BaseModTypeType):
  root = None

  def __init__(self):
    self.mods = list()

    class Modifier:
      def __init__(self, value):
        self.value = value
    
    self.Modifier = Modifier

  def modify(self, value):
    if self.mods:
      return value + self.mods[0].value
    return value

  def add(self, value):
    modifier = self.Modifier(value)
    self.mods.append(modifier)
    self.mods.sort()
    return modifier
  
  def remove(self, mod):
    self.mods.remove(mod)
