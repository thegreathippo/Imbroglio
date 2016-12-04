#Parser Testing
##TODO

###Parser Core Tests
- ~~Ensure instances of Parser produce appropriate functions when called with an infix expression (string).~~
  - ~~Function returns the resolved (correct) value of this expression.~~
    - ~~For simple equations.~~
    - ~~For complex (nested parenthetical) equations.~~
    - ~~For equations including floats.~~
- ~~When instanced with a dictionary (d) and integer (i), variables (v) will be retrieved from the dictionary: d[v][i]~~
  - We may actually adjust this later, to make Parser more general purpose.
- Do our internal 'custom' pointer-like objects (```_Internal```) carry a risk of allowing references to live on after they should be garbage-collected? We need to create a test to determine this (will be tricky).

###Parser Joint Tests

###Parser Internal Tests
- Ensure Parser correctly formats strings for evaluation.
- Ensure Parser correctly converts from infix to RPN.
- Ensure multiplication, addition, subtraction, exponents, and division all work appropriately.

###Parser Error Handling
