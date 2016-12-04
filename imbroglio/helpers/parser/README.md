#Parser
##TODO
##Questions/Notes
- Namespace for parsed expressions is currently handled via "."; this is used even for dictionary references (```component["x"][entity]``` is ```component.x.entity```). We ought to expand ```_Internal``` to handle keyword retrievals as well as attributes (also allow it to parse multiple references; ```component["x"][entities.player]```, for example.
- Are we at risk of having these dynamically constructed functions maintaining cyclical references? There should be some ways to test this. If we are, weakref should provide an easy solution.
