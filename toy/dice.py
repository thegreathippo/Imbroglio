import random
import collections

DiceResult = collections.namedtuple("DiceResult", ["value", "rolls", "raw"])

class Dice:
  
  def __init__(self, face):
    self.face = face

  def __call__(self, num=1, vantage=None):
    rolls = list()
    raw = list()
    for i in range(0, num):
      if vantage is None:
        roll = self._roll_die()
        rolls.append(roll)
      elif vantage is True:
        roll = self._roll_with_advantage()
        rolls.append(roll[0])
      else:
        roll = self._roll_with_disadvantage()
        rolls.append(roll[0])
      raw.append(roll)
    value = sum(rolls)
    return DiceResult(value=value, rolls=rolls, raw=raw)

  def _roll_die(self):
    return random.randint(1, self.face)

  def _roll_with_advantage(self):
    dice = self._roll_die(), self._roll_die()
    return sorted(list(dice), reverse=True)
  
  def _roll_with_disadvantage(self):
    dice = self._roll_die(), self._roll_die()
    return sorted(list(dice))
