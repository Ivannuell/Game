from entities.entity import Entity
from components.components import *


class Bullet(Entity):
    def __init__(self, game):
        super().__init__()

        self.__qualname__ = "Bullet"

        self.add_component(Position(100, 600))
        self.add_component(Velocity(10))
        self.add_component(Sprite())
        self.add_component(Animation(
            spritesheet="bullet",
            animation={
                "bullet": Anim([], [(0, 0, 6, 9)], 0, 0.2)
            }
        ))
        self.add_component(CollisionIdentity(
            layer=[CollisionID.Projectiles],
            mask=[CollisionID.Enemies, CollisionID.Obstacles]

        ))

        self.add_component(Collider(6, 9))

        self.game = game
        self.init_Entity()
