# TODO

## General
- OVERALL
  - config.py to store important constants
- Entities
  - Change entity keyword (passed to parser) to constant. Remember: You'll have to update the unitcode to reflect this, too! (use config.py)
  - Entity Destruction? Removal of all components from an entity?
  - Documentation
- Modifiers
  - Simplify/Document Modifier types and how they work.
    - Modifier types: Additive, Multiplicative, Function?
    - Define how I want users to add a modifier (and remove a modifier), then create the code to support that useage.
  - Documentation (wait, because we're going to rewrite this a lot, probably)
- System
  - Attributes to system instances which are classes...
    - Value
      - Shouldn't be offered so publicly; only provided because downstream classes need it.
    - Process
      - Must be public, because of automatic process registration (via inheritance)
    - Entity
      - Could have a method access this instead (`System.entity`) and keep it private (`System._entity_cls`).
    - ModType
      - Offered so you can subclass ModTypes. Might handle this like Process, might not, depends on how we decide user interface for modifiers will ultimately work.
- Process
  - Documentation
- Parser
  - Institute variable function argument number code
    - Operations (operators and functions) define how many values they want.
    - All operators take 2, functions take however many are in the parenthesis.  
  - Institute tuple returns (commas outside of parenthesis)
    - You might use the arg_counter function you wrote for this; might use it for the above, too!
  - Documentation

## Unit Testing
- Modifiers
  - Test Modifier persistence?
- Entities
  - When a component is set to None, its value should become the default for that entity
- Parser
  - Once we institute variable function argument code, we'll need to test it.
  - We'll want to restore the Parser tests in general, as well.
    - (You'll probably want to do this BEFORE you start editing the Parser).

## Error Handling
- At some point, describe (via documentation) our philosophy of error handling:
  - If something will cause an error eventually -- but not yet -- do it, _then_ raise the exception.
  - This way, it's possible to bypass the exception (but simultaneously, we protect from absurd behavior)
  - Example to use: Noncallable processes and noncallable hooks.
- Noncallable Process should raise an exception.
  - (So should all hooks if they are not callable!)
  - (But this should be done at the end; do all the operations, then raise the exception -- so we can bypass the exception if for some reason we want non-callable hooks)
    
