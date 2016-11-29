# TODO

## Basic Modules
These modules provide broad-purpose functionality for the core engine.

### Parser
The Parser module provides a Parser object; this object accepts an infix expression (as a string) and produces a callable object (formula) which, when called, evaluates the expression (returning either a single value or a tuple of values). Parser objects accept keyword assignments; these keywords become the 'namespace' for the expression.

*Dependencies*: None.
+ *core unit-test*: Not yet.
+ *core module*: Not yet.
+ *documentation*: Not yet.
+ *peripheral tests*: Not yet.

### Reader
The Reader module opens a file and evaluates its contents based on a lightweight ruleset to produce a dictionary of organized values (strings, ints, floats, lists, sets, and dictionaries). 

*Dependencies*: None.
+ *core unit-test*: Not yet.
+ *core module*: Not yet.
+ *documentation*: Not yet.
+ *peripheral tests*: Not yet.


## Entity Modules
These modules provide the architecture to construct entities based on data-defined components.

### Entities
The Entities module reads a component data file, creating Component Types from them; as each entity is defined with one or more components, it uses the Component Types to 


links to examine:
https://gist.github.com/JAForbes/99c15c0995b87a22b95a


