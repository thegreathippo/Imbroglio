from dice import Dice

class Check:
  FUMB, FAIL, SUCC, CRIT = -1, 0, 1, 2

  def __init__(self, actor_attr, target_attr):
    self.actor_attr = actor_attr
    self.target_attr = target_attr
    self.die = Dice(20)

  def __call__(self, actor, target, vantage=None):
    bonus = getattr(actor, self.actor_attr)
    dc = getattr(target, self.target_attr)
    roll = self.die(1, vantage)
    value = roll.value + bonus


