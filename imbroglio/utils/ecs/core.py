# Entity-Component architecture based loosely on JAForbes' idea:
# https://gist.github.com/JAForbes/99c15c0995b87a22b95a

world = 0
player = 1
monster = 2


class AspectType(type):
  """Metaclass for Aspects."""
  def __new__(cls, name, bases, namespace):
    new_cls = super().__new__(cls, name, bases, namespace)
    if new_cls.root:
      new_cls.root.add_aspect(new_cls)
    return new_cls


class BaseAspect(dict, metaclass=AspectType):
  """Base class for Aspects."""
  domain = {}
  priority = 0
  root = None

  def __init__(self):
    super().__init__()
    self.update({k:v for k, v in self.root.items() if k in self.domain})
    if not set(self.domain).issubset(self.root.keys()):
      # write a more descriptive exception later
      raise Exception("{0} instanced with invalid domain ({1})".format(self, self.domain))

  def setup(self):
    pass
  
  def process(self):
    self.setup()
    for uid in self._get_uids():
      self.run(uid)
    self.teardown()

  def run(self, uid):
    print(str(self) + ": " + str(uid))

  def teardown(self):
    pass

  def _get_uids(self):
    if self:
      return list(set.intersection(*[set(s) for s in self.values()]))
    return list()
