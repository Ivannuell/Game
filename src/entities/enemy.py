from entities.entity import Entity
from components.components import *

class Enemy(Entity):
    def __init__(self, config, game):
        super().__init__(game)

        self.__qualname__ = "Enemy"

        self.add(Animation(config["Animation"]["animation"], config["Animation"]["spritesheet"]))
        self.add(Position(config["Position"][0], config["Position"][1]))
        self.add(Velocity(config["Velocity"]))
        self.add(Size(config["Size"][0], config["Size"][1], config["Size"][2]))
        self.add(Collider(config["Collider"][0], config["Collider"][1]))
        self.add(Health(config["Health"]))
        self.add(Cannon(config["Cannon"]))

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

        self.init_Entity()