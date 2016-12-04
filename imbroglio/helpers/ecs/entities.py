"""Entity module for Imbroglio's ecs (Entity Component architecture).

This module provides access to the Entities and EntityHandler classes; 
Entities inherits from Python 3.x's dictionary, and effectively just 
has a unique __getitem__ method (if the returning value is callable, it
calls it and returns the result). EntityHandler provides a clean 
interface to retrieve an entity's components via attribute access 
(entity.x == components["x"][entity]).

TODO:
  * None, as of now (?)
"""
class Entities(dict):

  def __getitem__(self, key):
    item = super().__getitem__(key)
    if callable(item):
      return item()
    return item


class EntityHandler:
  def __init__(self, uid, _dict):
    self._uid = uid
    self._dict = _dict

  def __getattr__(self, attr):
    return self._dict[attr][self._uid]
