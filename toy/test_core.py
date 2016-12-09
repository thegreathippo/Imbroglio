"""
TODO:
  * Attempting to retrieve a non-existent component should...
    * Raise an attribute error for the entity?
    * Raise a custom error?
  * Test Modifier persistence?
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""
import unittest
from ecs import System


class CoreEntityTest(unittest.TestCase):
  def setUp(self):
    self.x, self.y, self.z = 1, 2, 3
    self.w = self.x + self.y
    self.system = System(x=self.x, y=self.y, z=self.z, 
                          w="{entity.x + entity.y}")
    self.entity = self.system.Entity(x=None, y=None, z=None, w=None)
    self._died = False

    class MagicMod(self.system.ModType):
      pass

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
    """Adding a modifier changes the entity's component's output value."""
    self.entity["x"].MagicMod.add(2)
    self.assertEqual(self.entity.x, self.x + 2)
    self.assertEqual(self.entity["x"].base, self.x)

  def test_entity_remove_modifier(self):
    """Removing a modifier reverts the entity's component's output value."""
    magicmod = self.entity["x"].MagicMod.add(2)
    self.entity["x"].MagicMod.remove(magicmod)
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



unittest.main()

