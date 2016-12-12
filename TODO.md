# TODO

## General
- ENTITIES
  - Change entity keyword (passed to parser) to constant. Remember: You'll have to update the unitcode to reflect this, too!
    - Which reminds me: config.py to store important constants!
  - Entity Destruction? Removal of all components from an entity?
- MODIFIERS
  - Simplify/Document Modifier types and how they work.
    - Modifier types: Additive, Multiplicative, Function?
    - Define how I want users to add a modifier (and remove a modifier), then create the code to support that useage.
- SYSTEM
  - Attributes to system instances which are classes...
    - Value
      - Shouldn't be offered so publicly; only provided because downstream classes need it.
    - Process
      - Must be public, because of automatic process registration (via inheritance)
    - Entity
      - Could have a method access this instead (`System.entity`) and keep it private (`System._entity_cls`).
    - ModType
      - Offered so you can subclass ModTypes. Might handle this like Process, might not, depends on how we decide user interface for modifiers will ultimately work.
    
## Unit Testing
- Modifiers
  - Test Modifier persistence?
- Entities
  - When a component is set to None, its value should become the default for that entity

## Error Handling
