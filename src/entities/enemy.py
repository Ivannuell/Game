from entities.entity import Entity
from components.components import *

class Enemy(Entity):
    def __init__(self, config):
        super().__init__()

        self.__qualname__ = "Enemy"

        self.add(config["Animation"])
        self.add(config["Position"])
        self.add(config["Velocity"])
        self.add(config["Size"])
        self.add(config["Collider"])
        self.add(config["Health"])
        self.add(config["Cannon"])

        self.add(CollidedWith())
        self.add(Sprite())
        self.add(EnemyIntent())
        self.add(MovementIntent())
        self.add(FireIntent())
        self.add(Rotation())
        self.add(ViewPosition())

        self.add(FactionIdentity("ENEMY"))
        self.add(CollisionIdentity(
            role="ENEMY",
            layer = [CollisionID.Enemies],
            mask = [CollisionID.Players, CollisionID.Projectiles]
        ))