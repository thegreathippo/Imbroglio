from ecs import System



world = System(x=0, y=0, z="{entity.x + entity.y}", name="default")


def start_world():
  player = world.Entity(x=5, y=3, z=None, name="player1")
  player2 = world.Entity(x=4, y=2, name="player2")
  print(player.z)


start_world()
