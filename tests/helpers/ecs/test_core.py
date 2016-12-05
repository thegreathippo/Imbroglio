"""
TODO:
  * Break this apart (core, aspects, entities?) into smaller tests.
  * Test for concurrent component instances...
    * Ensure entity equality doesn't cross over.
  * Test entity equality.
  * Test entity attribute assignment.
"""
import unittest
from ecs import Components


class CoreComponentTest(unittest.TestCase):
  def setUp(self):
    self.component = Components(x=0, y=0, z=0, w="{entity.x + entity.y}")

  def test_set_component_value_on_entity(self):
    """Test to ensure Component.set_components allows you to
    assign a component's value to an entity.
    """
    entity = 0
    self.component.set_components(entity, x=1)
    self.assertEqual(self.component["x"][entity], 1)

  def test_set_component_on_entity(self):
    """Test to ensure Component.set_components allows you to 
    add a component to an entity (setting it to the component's
    default value).
    """
    entity = 0
    self.component.set_components(entity, "x")
    self.assertEqual(self.component["x"][entity], 0)

  def test_set_component_and_component_value_on_entity(self):
    """Test to ensure Component.set_components allows you to both
    assign a component value and add a component to an entity.
    """
    entity = 0
    self.component.set_components(entity, "x", y=1)
    self.assertEqual(self.component["x"][entity], 0)
    self.assertEqual(self.component["y"][entity], 1)

  def test_set_component_formula_on_entity(self):
    """Test to ensure Component.set_components allows you to activate 
    a component's default value on an entity when that value is a formula.
    """
    entity = 0
    self.component.set_components(entity, "w", x=1, y=2)
    self.assertEqual(self.component["w"][entity], 3)

  def test_set_component_value_on_entity_to_formula(self):
    """Test to ensure Component.set_components allows you to assign assign
    a formula to an entity's component value.
    """
    entity = 0
    self.component.set_components(entity, x=1, y=2, w="{entity.x + entity.y}")
    self.assertEqual(self.component["w"][entity], 3)

  def test_aspect_priority(self):
    """Test to ensure priority class variable determines order of
    aspect setup.
    """
    test_list = []

    class AspectLast(self.component.Aspect):
      priority = 10

      def setup(self):
        test_list.append("last")

    class AspectFirst(self.component.Aspect):
      priority = -1

      def setup(self):
        test_list.append("first")

    class AspectMiddle(self.component.Aspect):

      def setup(self):
        test_list.append("middle")

    self.component.run()
    self.assertEqual(["first", "middle", "last"], test_list)

  def test_aspect_hooks_execute_in_order(self):
    """Test to ensure hook methods (startup, setup, run, teardown)
    execute in correct order, and correct number of times
    """
  
    test_list = []
    entity_1 = 0
    entity_2 = 1
    
    class AspectX(self.component.Aspect):
      domain = {"x"}
      
      def startup(self):
        test_list.append("startup")
      
      def setup(self):
        test_list.append("setup")
      
      def run(self, entity):
        test_list.append("run")
      
      def teardown(self):
        test_list.append("teardown")
      
    self.component.set_components(entity_1, x=10)
    self.component.set_components(entity_2, x=11)
    self.component.run()
    self.assertEqual(["startup", "setup", "run", "run", "teardown"], test_list)

  def test_aspect_hooks_execute(self):
    """Test to ensure hook methods (startup, setup, teardown)
    execute even when no components for this aspect exist
    """
    
    test_list = []
    
    class AspectX(self.component.Aspect):
      domain = {"x"}
      
      def startup(self):
        test_list.append("startup")
      
      def setup(self):
        test_list.append("setup")
      
      def run(self, entity):
        test_list.append("run")
      
      def teardown(self):
        test_list.append("teardown")
      
    self.component.run()
    self.assertEqual(["startup", "setup", "teardown"], test_list)

  def test_aspect_iteration(self):
    """Test to ensure aspects iterate over an entity when it gains
    a component in the aspect's domain, and aspects cease to iterate 
    when an entity loses that component.
    """
    test_list = []
    entity = 0
    
    class AspectX(self.component.Aspect):
      domain = {"x"}
      
      def run(self, entity):
        test_list.append("executed")
    
    self.component.set_components(entity, x=0)
    self.component.run()
    self.component.remove_components(entity, "x")
    self.component.run()
    self.assertEqual(["executed"], test_list)

  def test_aspect_entity_intersections(self):
    """Test to ensure that aspects iterate over entities that have 
    all the components in their domain, and not entities that only 
    have *some* components in their domain.
    """
    test_list = []
    entity_1 = 0
    entity_2 = 1
    entity_3 = 2
    
    class AspectXY(self.component.Aspect):
      domain = {"x", "y"}
      
      def run(self, entity):
        test_list.append(entity.get_uid())

    self.component.set_components(entity_1, x=0, y=0)
    self.component.set_components(entity_2, x=0)
    self.component.run()
    self.component.remove_components(entity_1, "x")
    self.component.set_components(entity_2, y=0)
    self.component.run()
    self.assertEqual([entity_1, entity_2], test_list)


unittest.main()
