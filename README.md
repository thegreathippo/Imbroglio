# Imbroglio
imbroglio is an entity-component system designed for numerous objects (entities) with very similar properties (components) that are handled by independent systems (processes) based on which objects have which properties.

## Overview
imbroglio's System class creates a custom dictionary that tracks which component values are associated with which entities (which are associated with which values). In other words, rather than storing components like this...

~~~~{"player" : {"x" : 5, "y" : 6}, "monster": {"x" : 7, "y": 9}}

~~~~

...imbroglio stores components like this:

``{"x" : {"player" : 5, "monster" : 7}, "y" : {"player" : 6, "monster" : 9}}``

This way, imbroglio doesn't need to iterate over every entity to determine if they have the correct components; rather, it goes straight to the component and begins iterating over the relevant entities.

The disadvantage of this approach is that referring to an entity's components becomes cumbersome and counter-intuitive. Rather than this...

``entities["player"]["x"]``

...we need to do this:

``components["x"]["player"]``

Much of imbroglio's 'magic' is dedicated to maintaining the computational advantages of the second approach while providing the intuitiveness of the first approach.

In addition to this, imbroglio offers a way to store an entity's component-value as a formula (similar to Python's @property decorator, or custom __get__ descriptors), and a way to define 'modifer-types' which can (temporarily) modify a component's value.

## Important Links
http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
