#ECS system
##TODO
- Need a way to create 'new' entities.
  - Keeping in mind, entities should be made via aspects, not components.
  - Otherwise, there's a risk of entities without the right components to touch a process.
- A type of domain that automatically cycles through [i]all[/i] entities?
  - A component that all entities have (until they don't have anything but that component?)
  - If so, we might make this component/aspect generated in the Components class.
- Templating system (?).
  - Is it separate? Or part of ECS? A helper?
##QUESTIONS
- Should the entities dictionaries 'know' the component dictionaries they're part of? Why?
