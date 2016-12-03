#ECS Testing
##TODO
###ECS Core Tests
- ~~Ensure aspects iterate over correct entities.~~
  - ~~When an entity is assigned components that an aspect owns, the aspect iterates over it.~~
  - ~~When an entity has one of these components removed, the aspect no longer iterates over it.~~
- ~~Ensure aspects iterate in correct order.~~
  - ~~An aspect's priority class variable determines the order in which it executes.~~
- ~~Ensure aspects perform startup, setup, execute, teardown, shutdown in right order.~~
  - ~~And that they do these things the 'correct' number of times.~~
  - ~~Also, startup, setup, teardown, and shutdown all occur even if execute doesn't (no entities overlap).~~

###ECS Joint Tests
- Parser and ECS
 - Test a formula-function to ensure it produces the expected result.

###ECS Internal Tests 
- If setup returns X, we skip the execute order (don't even bother running get_uids).


###ECS Error Handling
