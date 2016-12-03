import unittest
from ecs import Components


class CoreComponentTest(unittest.TestCase):
  def setUp(self):
    self.component = Components("x", "y", "z")

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
      
      def run(self, uid):
        test_list.append("run")
      
      def teardown(self):
        test_list.append("teardown")
      
    self.component["x"][entity_1] = 10
    self.component["x"][entity_2] = 11
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
      
      def run(self, uid):
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
      
      def run(self, uid):
        test_list.append("executed")
    
    self.component["x"][entity] = 0
    self.component.run()
    del self.component["x"][entity]
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
      
      def run(self, uid):
        test_list.append(uid)
    
    self.component["x"][entity_1] = 0
    self.component["y"][entity_1] = 0
    self.component["x"][entity_2] = 0
    self.component.run()
    del self.component["x"][0]
    self.component["y"][entity_2] = 0
    self.component.run()
    self.assertEqual([entity_1, entity_2], test_list)

unittest.main()
