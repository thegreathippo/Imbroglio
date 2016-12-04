import unittest
from ...imbroglio.helper.reader import load_components


class CoreComponentTest(unittest.TestCase):
  def setUp(self):
    self.entity = 0
    self.component = load_components("components.dat")

  def test_component_default_values(self):
    self.component.set_components(self.entity, "strength")
    self.assertEqual(self.component["strength"][self.entity], 14)

  def test_component_set_values(self):
    self.component.set_components(self.entity, strength=10)
    self.assertEqual(self.component["strength"][self.entity], 10)
  
  def test_component_default_formula(self):
    self.component.set_components(self.entity, "strength", "str_bonus")
    self.assertEqual(self.component["str_bonus"][self.entity], 2)

  def test_component_set_formula(self):
    self.component.set_components(self.entity, "strength", str_bonus="{entity.strength * 2}")
    self.assertEqual(self.component["str_bonus"][self.entity], 28)

  def test_component_formula_refers_to_other_formula(self):
    self.component.set_components(self.entity, "strength", "str_bonus", "str_super_bonus")
    self.assertEqual(self.component["str_super_bonus"][self.entity], 16)

unittest.main()
