import operations
import re
from weakref import WeakValueDictionary

L, R = operations.L, operations.R
LEFT, RIGHT = operations.LEFT, operations.RIGHT
operators, functions = operations.operators, operations.functions


class Parser:
  def __init__(self, **namespace):
    """Instance a Parser object with a given namespace."""
    self._namespace = WeakValueDictionary(namespace)
    o_func = {k:v[0] for k, v in operators.items()}
    f_func = {k:v[0] for k, v in functions.items()}
    self.operations = {**o_func, **f_func}
    self._operators = set(operators)
    self._functions = set(functions)
    self._precedence = {k:v[1] for k, v in operators.items()}
    self._left = {o for o in operators if operators[o][2] == L}
    self._right = {o for o in operators if operators[o][2] == R}

    class Internal(_Internal):
      namespace = dict(self._namespace)

    self.Internal = Internal

  def __call__(self, text):
    """Return a function that, when called, will evaluate the supplied 
    text as an infix expression and return the result. 
    """
    rpn = self.rpn(text)
    def func():
      stack = _Stack()
      for token in rpn:
        if token in self.operations:
          val2, val1 = stack.pop(), stack.pop()
          stack.push(self.operations[token](val1, val2))
        else:
          if callable(token):
            stack.push(token())
          else:
            stack.push(token)
      return stack[0]
    return func

  def rpn(self, text):
    """Translate an infix expression (given as a string) into
    reverse polish notation (RPN) using the parser instance's
    particular operation precedence and associativity rules.
    """
    output = []
    stack = _Stack()

    def pop_operator(t):
        o = stack.get_top()
        if o in self._operators:
            t_pre, o_pre = self._precedence[t], self._precedence[o]
            if ((t in self._left and t_pre <= o_pre) or
                    (t in self._right and t_pre < o_pre)):
                output.append(stack.pop())
                return pop_operator(t)

    def pop_parenthesis(t):
        top = stack.get_top()
        if top is None:
            raise Exception("Mismatched ()")
        if top == "(":
            stack.pop()
            if stack.get_top() in self._functions:
                output.append(stack.pop())
            return
        output.append(stack.pop())
        return pop_parenthesis(t)

    formatted = _format(self._operators, text)
    for token in formatted:
        if _is_int(token):
            output.append(int(token))
        elif _is_float(token):
            output.append(float(token))
        elif token in self._functions:
            stack.push(token)
        elif token == ",":
            while stack.get_top() != "(":
                output.append(stack.pop())
        elif token in self._operators:
            pop_operator(token)
            stack.push(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            pop_parenthesis(token)
        else:
            matching = [s for s in self._namespace if token.startswith(s)]
            if matching:
              output.append(self.Internal(token))
    for o in reversed(stack):
        output.append(stack.pop())
    return output


class _Stack(list):

    def push(self, item):
        self.append(item)

    def get_top(self):
        if len(self) > 0:
            return self[-1]


class _Internal:
  namespace = dict()

  def __init__(self, path):
      _path = path.split(".")
      self.root = _path[0]
      self.path = _path[1:]

  def __call__(self):
      value = self.namespace[self.root]
      for step in self.path:
        if step in self.namespace:
          step = self.namespace[step]
        try:
          value = getattr(value, step)
        except (AttributeError, TypeError):
          value = value[step]
      return value

def _is_int(token):
    try:
        int(token)
        return True
    except ValueError:
        return False

def _is_float(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def _format(operators, text):
  pattern = "([( )," + "".join(operators) + "])"
  if "-" in pattern:
    i = pattern.index("-")
    pattern = pattern[:i] + "\\" + pattern[i:]
  raw = re.split(pattern, text)
  return [e for e in raw if e != " " and e != ""]
