import unittest
from ...helpers.parser import Parser

# Simple test.
test1_inf = "(12 - 3 ) / 3^2 + 2 * 3"
test1_ans = 7

# Complex test.
test2_inf = "( ( 1  + 2 ) / 3 ) ^ (4 * 6)"
test2_ans = 1

# Float test.
test3_inf = "( 1 + 2 ) * ( 3 / 4 ) ^ ( 5 + 6 )"
test3_ans = 0.12670540809631348

# Function test.
test4_inf = "max((2 + 3) / 5 * min(5, 2 + 2), 10)"
test4_ans = 10

# Everything test.
test5_inf = "((5 + min(max(self.x, 9), 11)) / 5)^2"
test5_ans = 9

class CoreParserTest(unittest.TestCase):
  def setUp(self):
    self.tester = 0
    self.components = {"x" : {self.tester : 10}}
    self.parser = Parser(self.components)

  def test_parser_returns_callable(self):
    """Test to ensure the parser returns a callable function."""
    func = self.parser("", 0)
    self.assertTrue(callable(func))

  def test_simple_answer(self):
    """Test to ensure the parser's function resolves simple 
    expressions correctly.
    """
    answer = self.parser(test1_inf, self.tester)
    self.assertEqual(test1_ans, answer())

  def test_complex_answer(self):
    """Test to ensure the parser's function resolves complex 
    expressions correctly.
    """
    answer = self.parser(test2_inf, self.tester)
    self.assertEqual(test2_ans, answer())

  def test_float_answer(self):
    """Test to ensure the parser's function resolves expressions
    with floats correctly.
    """
    answer = self.parser(test3_inf, self.tester)
    self.assertAlmostEqual(test3_ans, answer())

  def test_function_answer(self):
    """Test to ensure the parser's function resolves expressions
    with functions correctly.
    """
    answer = self.parser(test4_inf, self.tester)
    self.assertEqual(test4_ans, answer())

  def test_can_access_component_value(self):
    """Test to ensure the parser's function can access component
    values correctly.
    """
    answer = self.parser("self.x", self.tester)
    self.assertEqual(10, answer())

  def test_everything(self):
    """Test to ensure the parser's function can resolve an 
    expression that contains all the features described above.
    """
    answer = self.parser(test5_inf, self.tester)
    self.assertEqual(test5_ans, answer())

unittest.main()
