# TODO

## General
* Change entity keyword to constant
 * In both the unit test and the primary code, we should make it so that instead of loading 'entity' into the namespace of our parser, we load a constant (which we can therefore change later if we prefer).
* Modifer types: Additive, Multiplicative, Function?
 * This means breaking modifiers down into more precise types to make them easier to understand and deploy.
 * We might encounter some problems regarding how multipliers are 'handled' (how they work when multiple multipliers of the same type are present), but we could have the 'function' type handle all of these weirder cases? Or not?
* Entity Destruction? Removal of all components from an entity?
* Investigate ways to move the System instance's class attributes (Value, Entity, etc) out of sight without just making them private? And still provide access to the lower level instances where needed? Allowing us to access 'Entity' via a method instead of directly instancing the class?


## Error Handling
