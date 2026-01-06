from entities.entity import Entity
from components.components import *

class Enemy(Entity):
    def __init__(self, game = None):
        super().__init__()

        self.__qualname__ = "Enemy"

        self.add(Animation(
            spritesheet="ship",
            animation = {
                "ship-idle": Anim([], [(0,0,48,48)], 0, 0.2)
            }
        ))
        self.add(CollisionIdentity(
            layer = [CollisionID.Enemies],
            mask = [CollisionID.Players, CollisionID.Projectiles]
        ))
        self.add(Position(500, 100))
        self.add(Velocity(50))
        self.add(Size(48,48,2))
        self.add(Sprite())
        self.add(Collider())
        # self.add(Solid())

        self.add(Health(100))

        self.add(EnemyIntent())
        self.add(MovementIntent())
        self.add(FireIntent())
        self.add(Cannon(0.4))
        self.add(Rotation())
        self.add(ViewPosition())

        self.add(FactionIdentity("ENEMY"))