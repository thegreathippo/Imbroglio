# Examples

## Basics
Let's start by importing `imbroglio`'s core system.
~~~~
>>> from ecs import System
>>> world = System(x=0, y=0)
~~~~
The `System` instance accepts any number of keyword arguments; the keywords become components within that system, while the values become the default values for those components.

To create an entity, we must instance the `System` instance's `Entity` class. Keyword arguments passed to this class will set these components to these values.
~~~~
>>> player = world.Entity(x=5, y=6)
>>> world["x"][player]
5
~~~~
This new instance provides access to the associated components via its attributes.
~~~~
>>> player.x
5
>>> world["x"][player]
5
>>> player.x = 6
>>> player.x
6
>>> world["x"][player]
6
~~~
However, the actual components are not stored on the entity itself:
~~~~
>>> "x" in player.__dict__
False
~~~~
They're stored inside the `System` instance; the `Entity` instance only provides a simple interface to manipulate the data on a `System` instance (via the `Entity` instance's `__setattr__`, `__getattr___`, and `__delattr__` methods).

Instancing an entity with a component set to `None` will result in the component being set to whatever the `System` instance has defined as the default value for that component:
~~~~
>>> world = System(x=5, y=6)
>>> player = world.Entity(x=0, y=None)
>>> player.x
0
>>> player.y
6
~~~~
When you instance an `Entity` class, you are doing one of two things: Creating a new entity or retrieving a pre-existing entity. Which is occurring depends on whether or not you pass a positional value to the `Entity` class.
~~~~
>>> world = System(x=5, y=6)
>>> player = world.Entity(x=0, y=3)
>>> player2 = world.Entity(player)
>>> player.x
0
>>> player2.x
0
~~~~
