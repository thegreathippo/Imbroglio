# Imbroglio
`imbroglio` is an entity-component system designed to manipulate numerous objects (entities) with certain attributes (components) via independent systems (processes) which select which objects to manipulate based on whether or not an object has attributes relevant to that system.

## Overview
`imbroglio`'s `System` class creates a custom dictionary that tracks which component values are associated with which entities (which are associated with which values). In other words, rather than storing components like this...
~~~~
{"player": 
    {"x": 5, 
     "y": 6}, 
 "monster": 
    {"x": 7, 
     "y": 9}}
~~~~
...`imbroglio` stores components like this:
~~~~
{"x": 
    {"player": 5, 
     "monster": 7}, 
 "y": 
    {"player": 6, 
     "monster": 9}}
~~~~
This way, `imbroglio` doesn't need to iterate over every entity to determine if they have the correct components; rather, it goes straight to the component and begins iterating over the relevant entities.

The disadvantage of this approach is that referring to an entity's components becomes cumbersome and counter-intuitive. Rather than this...

`entity.x = 6`

...we need to do this:

`components["x"][entity] = 6`

Much of `imbroglio`'s 'magic' is dedicated to maintaining the computational advantages of the second approach while providing the intuitiveness of the first approach (without storing extra data, and without creating cyclical references).

In addition to this, `imbroglio` offers a way to store an entity's component-value as a formula (similar to Python's `@property` decorator, or custom `__get__` descriptors), and a way to define 'modifer-types' which can (temporarily) modify a component's value.

## Important Links
http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
