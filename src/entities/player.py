
from entities.entity import Entity

from components.components import *


class Player(Entity):
    def __init__(self, config):
        super().__init__()

        self.__qualname__ = "Player"

        self.add(Animation(
            spritesheet=config["Sprite"],
            animation = config["Anim"]
        ))
        self.add(Position(config["Pos"][0], config["Pos"][1]))
        self.add(Velocity(config["Vel"]))
        self.add(Size(48,48))
        self.add(Sprite())
        self.add(MovementIntent())
        self.add(Collider())
        self.add(InputControlled())
        self.add(FireIntent())
        self.add(FactionIdentity("PLAYER"))
        self.add(CollisionIdentity(
            layer = [CollisionID.Players], 
            mask = [CollisionID.Enemies, CollisionID.Projectiles] 
        ))

        if "Cannon" in config:
            self.add(Cannon(0.3))

        self.add(Health(500))
        self.add(Rotation())
        self.add(ViewPosition())
