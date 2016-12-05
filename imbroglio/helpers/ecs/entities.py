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


class BaseEntity:
  root = None

  def __init__(self, uid):
    super().__setattr__("_uid", uid)

  def get_uid(self):
    return self._uid

  def __getattr__(self, attr):
    return self.root[attr][self._uid]

  def __setattr__(self, attr, value):
    self.root[attr][self._uid] = value
  
  def __hash__(self):
    return hash((self.get_uid(), type(self)))
  
  def __eq__(self, other):
    try:
      return ((other.get_uid(), type(other)) == (self.get_uid(), type(self)))
    except AttributeError:
      return False
