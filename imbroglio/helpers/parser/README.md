#Parser
##TODO
##Questions
- Should we change the way parser instances access entity components? Rather than supplying the entity identity (effectively just a key), maybe we should refer to entity components in data just as we refer to them in code: ```component["strength"][self]``` could be used, for example.
  - If we did this, component could be just a keyword assignment the parser is instanced with. We have to allow the parser to parse indexing/keyword getters, then, though.
- Are we at risk of having these dynamically constructed functions maintaining cyclical references? There should be some ways to test this.
