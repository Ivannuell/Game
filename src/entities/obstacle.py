from entities.entity import Entity
from components.components import *

class Obstacle(Entity):
    def __init__(self):
        super().__init__()

        self.__qualname__ = "Obstacle"

        self.add_component(Animation(
            frame_scale=3,
            spritesheet="ship",
            animation = {
                "ship-idle": Anim([], [(0,0,48,48)], 0, 0.2)
            }
        ))
        self.add_component(CollisionIdentity(
            layer = [CollisionID.Players, CollisionID.Enemies],
            mask = []
            
        ))
        self.add_component(Position(500, 10))
        self.add_component(Sprite())
        self.add_component(Collider(48,48))
        self.add_component(Solid())