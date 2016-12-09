"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
class _ProcessType(type):

  def __new__(cls, name, bases, namespace):
    new_cls = super().__new__(cls, name, bases, namespace)
    if new_cls.root:
      process = new_cls()
      new_cls.root.register_process(process.process, priority=process.priority,
                                    domain=process.domain, 
                                    startup=process.startup, 
                                    setup=process.setup, 
                                    teardown=process.teardown, 
                                    shutdown=process.shutdown)
    return new_cls


class BaseProcess(metaclass=_ProcessType):
  priority = 0
  domain = set()
  root = None
  
  def startup(self):
    pass
  
  def setup(self):
    pass
  
  def process(self, entity):
    pass
  
  def teardown(self):
    pass
  
  def shutdown(self):
    pass
