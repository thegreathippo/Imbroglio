import collections


class Modifiers:

  def __init__(self, owner):
    self.sources = {None: list()}
    self.innate = list()
    self.sources = collections.OrderedDict()
    root = self

    class _Mod:

      def __init__(self, value, func, source=None, *tags):
        self.value = owner.parse(value)
        self.func = func
        self.source = source
        self.tags = tags

      def __call__(self, value):
        return self.func(value, self.value)

      def remove(self):
        root.remove(self)

    self.Mod = _Mod
  
  def remove(self, mod):
    if mod.source:
      self.sources[mod.source].remove(mod)
    else:
      self.innate.remove(mod)

  def __call__(self, value, func, source=None, *tags):
    modifier = self.Mod(value, func, source, *tags)
    if modifier.source is None:
      self.innate.append(modifier)
    else:
      if source in self.sources:
        self.sources[source].append(modifier)
        sorted(self.sources[source], key=lambda x: x.value, reverse=True)
      else:
        self.sources[source] = [modifier]
    return modifier

  def modify(self, value):
    ret_value = value
    for mod in self.innate:
      ret_value = mod(ret_value)
    for mods in self.sources.values():
      mod = mods[0]
      ret_value = mod(ret_value)
    return ret_value

