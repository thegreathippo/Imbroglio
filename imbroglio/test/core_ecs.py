"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TODO:
  * Attempting to retrieve a non-existent component should...
    * Raise an attribute error for the entity?
    * Raise a custom error?
  * Test Modifier persistence?
  * When adding an attribute to an entity as None, default value?
  * Test for Modifier recursion (when a modifier adds the thing it's modifying)
    * Example: entity["x"].add("{entity.x}")
"""
import unittest
from ecs import System


class CoreRegisteredProcessTest(unittest.TestCase):
  """Test for manually registered processes."""

  def setUp(self):
    self.system = System(x=0, y=0)
    self.tracking = list()
    self.entity1 = self.system.Entity()
    self.entity2 = self.system.Entity()
    self.eid1 = self.entity1.get_eid()
    self.eid2 = self.entity2.get_eid()
    self.eid_tracking = {self.eid1: 0, self.eid2: 0}
    def startup1():
      self.tracking.append("startup1")
    def setup1():
      self.tracking.append("setup1")
    def process1(entity):
      self.tracking.append("process1")
      eid = entity.get_eid()
      self.eid_tracking[eid] += 1
    def teardown1():
      self.tracking.append("teardown1")
    def shutdown1():
      self.tracking.append("shutdown1")
    def startup2():
      self.tracking.append("startup2")
    def setup2():
      self.tracking.append("setup2")
    def process2(entity):
      self.tracking.append("process2")
      eid = entity.get_eid()
      self.eid_tracking[eid] += 1
    def teardown2():
      self.tracking.append("teardown2")
    def shutdown2():
      self.tracking.append("shutdown2")
    def startup3():
      self.tracking.append("startup3")
    def setup3():
      self.tracking.append("setup3")
    def process3(entity):
      self.tracking.append("process3")
      eid = entity.get_eid()
      self.eid_tracking[eid] += 1
    def teardown3():
      self.tracking.append("teardown3")
    def shutdown3():
      self.tracking.append("shutdown3")
    
    self.startup1, self.setup1 = startup1, setup1
    self.process1, self.teardown1 = process1, teardown1
    self.shutdown1 = shutdown1

    self.startup2, self.setup2 = startup2, setup2
    self.process2, self.teardown2 = process2, teardown2
    self.shutdown2 = shutdown2

    self.startup3, self.setup3 = startup3, setup3
    self.process3, self.teardown3 = process3, teardown3
    self.shutdown3 = shutdown3

  def register_all_processes(self):
    self.system.register_process(self.process2, domain={"x", "y"}, priority=2,
                                  setup=self.setup2, startup=self.startup2,
                                  teardown=self.teardown2, 
                                  shutdown=self.shutdown2)
    self.system.register_process(self.process3, domain={"x", "y"}, priority=3,
                                  setup=self.setup3, startup=self.startup3,
                                  teardown=self.teardown3, 
                                  shutdown=self.shutdown3)
    self.system.register_process(self.process1, domain={"x", "y"}, priority=1,
                                  setup=self.setup1, startup=self.startup1,
                                  teardown=self.teardown1, 
                                  shutdown=self.shutdown1)
  
  def run_system(self, iterations=1):
    for i in range(0, iterations):
      self.system.step()
    self.system.quit()

  def test_process_execution_on_correct_entities(self):
    """Processes execute on entities with correct components."""
    self.entity1.x, self.entity1.y = None, None
    self.entity2.x = None
    self.register_all_processes()
    self.run_system()
    self.assertEqual(self.eid_tracking, {self.eid1: 3, self.eid2 : 0})
  
  def test_process_execution_on_entities_when_component_removed(self):
    """Processes cease to execute on entities when they lose relevant components."""
    self.entity1.x, self.entity1.y = None, None
    self.entity2.x, self.entity2.y = None, None
    self.register_all_processes()
    self.system.step()
    del self.entity1.x
    self.system.step()
    self.assertEqual(self.eid_tracking, {self.eid1: 3, self.eid2: 6})

  def test_process_execution_on_entities_when_component_added(self):
    """Processes begin executing on entities when they gain relevant components."""
    self.entity1.x, self.entity1.y = None, None
    self.entity2.x = None
    self.register_all_processes()
    self.system.step()
    self.entity2.y = None
    self.system.step()
    self.assertEqual(self.eid_tracking, {self.eid1: 6, self.eid2: 3})

  def test_process_hook_execution_no_entities(self):
    """Process hooks execute in appropriate order (with no entities)"""
    self.register_all_processes()
    self.run_system(2)
    self.assertEqual(self.tracking, ["startup1", "startup2", "startup3", 
                                     "setup1", "teardown1", "setup2", 
                                     "teardown2", "setup3", "teardown3",
                                     "setup1", "teardown1", "setup2",
                                     "teardown2", "setup3", "teardown3",
                                     "shutdown1", "shutdown2", "shutdown3"])


  def test_process_hook_execution_with_entity(self):
    """Process hooks execute in appropriate order (with one entity)"""
    self.entity1.x, self.entity1.y = None, None
    self.register_all_processes()
    self.run_system()
    self.assertEqual(self.tracking, ["startup1", "startup2", "startup3", 
                                     "setup1", "process1", "teardown1", 
                                     "setup2", "process2", "teardown2",
                                     "setup3", "process3", "teardown3",
                                     "shutdown1", "shutdown2", "shutdown3"])

  def test_process_hook_execution_with_two_entities(self):
    """Process hooks execute in appropriate order (with two entities)"""
    self.entity1.x, self.entity1.y = None, None
    self.entity2.x, self.entity2.y = None, None
    self.register_all_processes()
    self.run_system()
    self.assertEqual(self.tracking, ["startup1", "startup2", "startup3", 
                                     "setup1", "process1", "process1", 
                                     "teardown1", "setup2", "process2", 
                                     "process2", "teardown2", "setup3", 
                                     "process3", "process3", "teardown3",
                                     "shutdown1", "shutdown2", "shutdown3"])


class CoreProcessTest(CoreRegisteredProcessTest):
  """Test for automatically registered processes."""

  def setUp(self):
    self.system = System(x=0, y=0)
    self.tracking = list()
    self.entity1 = self.system.Entity()
    self.entity2 = self.system.Entity()
    self.eid1 = self.entity1.get_eid()
    self.eid2 = self.entity2.get_eid()
    self.eid_tracking = {self.eid1: 0, self.eid2: 0}

    class Process1(self.system.Process):
      domain = {"x", "y"}
      terms = {
        "startup": "startup1",
        "setup": "setup1",
        "process": "process1",
        "teardown": "teardown1",
        "shutdown": "shutdown1"
              }
      def startup(cls):
        self.tracking.append(cls.terms["startup"])
      def setup(cls):
        self.tracking.append(cls.terms["setup"])
      def process(cls, entity):
        self.tracking.append(cls.terms["process"])
        eid = entity.get_eid()
        self.eid_tracking[eid] += 1
      def teardown(cls):
        self.tracking.append(cls.terms["teardown"])
      def shutdown(cls):
        self.tracking.append(cls.terms["shutdown"])

    class Process2(Process1):
      priority = 2
      terms = {
        "startup": "startup2",
        "setup": "setup2",
        "process": "process2",
        "teardown": "teardown2",
        "shutdown": "shutdown2"
              }

    class Process3(Process1):
      priority = 3
      terms = {
        "startup": "startup3",
        "setup": "setup3",
        "process": "process3",
        "teardown": "teardown3",
        "shutdown": "shutdown3"
              }


  def register_all_processes(self):
    pass


class CoreEntityTest(unittest.TestCase):
  """Test core entity behavior."""

  def setUp(self):
    self.x, self.y, self.z = 1, 2, 3
    self.w = self.x + self.y
    self.system = System(x=self.x, y=self.y, z=self.z, 
                          w="{entity.x + entity.y}")
    self.entity = self.system.Entity(x=None, y=None, z=None, w=None)
    self._died = False

  def test_defaults(self):
    """Entity instances with default values."""
    self.assertEqual(self.entity.x, self.x)
    self.assertEqual(self.entity.y, self.y)
    self.assertEqual(self.entity.z, self.z)
    self.assertEqual(self.entity.w, self.w)

  def test_change_entity_value(self):
    """Changing entity values updates component values appropriately."""
    self.entity.x = 5
    self.assertEqual(self.system["x"][self.entity](), 5)

  def test_entity_formula(self):
    """Changing relevant entity values also changes output of formulas."""
    self.entity.x = 5
    self.assertEqual(self.entity.w, 5 + self.y)

  def test_change_entity_formula(self):
    """Changing entity formulas changes output of formulas appropriately."""
    self.entity.w = "{entity.x + entity.x}"
    self.assertEqual(self.entity.w, self.x + self.x)

  def test_entity_death(self):
    """Entities do not persist."""
    def die(cls):
      self._died = True
    self.system.Entity.__del__ = die
    def run():
      entity = self.system.Entity(x=None, y=None, z=None, w=None)
    run()
    self.assertTrue(self._died)

  def test_entity_add_modifier(self):
    """Adding an add-modifier changes the entity's component's output."""
    mod = self.entity["x"].add(2)
    self.assertEqual(self.entity.x, self.x + 2)
    # Check to ensure base still remains the same.
    self.assertEqual(self.entity["x"].base, self.x)
    self.entity["x"].base = 0
    # Modifying the base should change the output without changing the mod.
    self.assertEqual(self.entity.x, 2)

  def test_entity_remove_add_modifier(self):
    """Removing an add-modifier reverts the entity's component's output."""
    mod = self.entity["x"].add(2)
    mod.remove()
    self.assertEqual(self.entity.x, self.x)
  
  def test_entity_add_formula_modifier(self):
    """Add-modifiers allow for formulas (just like components)."""
    mod = self.entity["x"].add("{entity.y * 2}")
    self.assertEqual(self.entity.x, self.x + self.entity.y * 2)

  def test_entity_remove_add_formula_modifier(self):
    """Removing an add-modifier formula reverts the entity's component value."""
    mod = self.entity["x"].add("{entity.y * 2}")
    mod.remove()
    self.assertEqual(self.entity.x, self.x)

  def test_entity_swap_modifier(self):
    """Adding a swap-modifier changes the entity's component's output."""
    mod = self.entity["x"].swap(self.y)
    self.assertEqual(self.entity.x, self.y)
    # Check to ensure the base still remains the same.
    self.assertEqual(self.entity["x"].base, self.x)
    self.entity["x"].base = 0
    # Modifying the base should NOT change the output.
    self.assertEqual(self.entity.x, self.y)

  def test_entity_remove_swap_modifier(self):
    """Removing a swap-modifier reverts the entity's component's output."""
    mod = self.entity["x"].swap(self.y)
    mod.remove()
    self.assertEqual(self.entity.x, self.x)
  
  def test_entity_swap_formula_modifier(self):
    """Swap-modifiers allow for formulas (just like components)."""
    mod = self.entity["x"].swap("{entity.y * 2}")
    self.assertEqual(self.entity.x, self.y * 2)

  def test_entity_remove_swap_formula_modifier(self):
    """Removing a swap-modifier formula reverts the entity's component value."""
    mod = self.entity["x"].swap("{entity.y * 2}")
    mod.remove()
    self.assertEqual(self.entity.x, self.x)

  def test_entity_equivalence(self):
    """Entities with the same eid are equivalent."""
    entity = self.system.Entity(self.entity.get_eid())
    self.assertEqual(entity.x, self.x)
    self.assertEqual(entity.y, self.y)
    self.assertEqual(entity.z, self.z)
    self.assertEqual(entity.w, self.w)
    entity.x = 5
    self.assertEqual(entity.x, 5)
    self.assertEqual(self.entity.x, 5)
    self.assertEqual(entity.w, 5 + self.y)
    self.assertEqual(self.entity.w, 5 + self.y)

  def test_entity_inequivalence(self):
    """Entities with different eids are not equivalent."""
    entity = self.system.Entity(x=self.x, y=self.y, z=self.z,
                                w="{entity.x + entity.y}")
    self.assertEqual(entity.x, self.entity.x)
    self.assertEqual(entity.y, self.entity.y)
    self.assertEqual(entity.z, self.entity.z)
    self.assertEqual(entity.w, self.entity.w)
    entity.x = -1
    self.assertNotEqual(entity.x, self.entity.x)
    self.assertNotEqual(entity.w, self.entity.w)
