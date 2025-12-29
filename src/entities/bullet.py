from entities.entity import Entity
from components.components import *


class Bullet(Entity):
    def __init__(self, game):
        super().__init__()

        self.__qualname__ = "Bullet"

        self.add(Position(100, 600))
        self.add(Velocity(10))
        self.add(Size(6,9,2))
        self.add(Sprite())
        self.add(Animation(
            spritesheet="bullet",
            animation={
                "bullet": Anim([], [(0, 0, 6, 9)], 0, 0.2)
            }
        ))
        self.add(CollisionIdentity(
            layer=[CollisionID.Projectiles],
            mask=[CollisionID.Enemies, CollisionID.Obstacles, CollisionID.Players]

        ))

        self.add(Collider())

        self.add(Damage(20))
        self.add(Rotation())
        self.add(ViewPosition())

        self.game = game
        self.init_Entity()
