from entities.entity import Entity
from components.components import *

class Obstacle(Entity):
    def __init__(self):
        super().__init__()

        self.__qualname__ = "Obstacle"

        self.add(Animation(
            spritesheet="ship",
            animation = {
                "ship-idle": Anim([], [(0,0,48,48)], 0, 0.2)
            }
        ))
        self.add(CollisionIdentity(
            layer = [CollisionID.Players, CollisionID.Enemies],
            mask = []
            
        ))

        self.add(Position(200, 500))
        self.add(Sprite())
        self.add(Size(48,48))
        self.add(Collider())
        self.add(Solid())
        self.add(FactionIdentity("Obstacle"))