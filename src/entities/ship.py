from entities.entity import Entity
from components.components import *

class Spaceship(Entity):
    def __init__(self, scene, config={}):
        super().__init__(scene)

        self.add(Animation(config["Animation"]["animation"], config["Animation"]["spritesheet"]))
        self.add(Position(config["Position"][0], config["Position"][1]))
        self.add(Velocity(config["Velocity"]))
        self.add(Size(config["Size"][0], config["Size"][1], config["Size"][2]))
        self.add(Collider(config["Collider"][0], config["Collider"][1]))
        self.add(Health(config["Health"]))

        self.add(CollidedWith())
        self.add(Sprite())
        self.add(MovementIntent())
        self.add(ShootIntent())
        self.add(Rotation())
        self.add(ViewPosition())
        self.add(Bot())

        self.add(GridCell())

        self.add(FactionIdentity(""))
        self.add(CollisionIdentity(
            role="",
            layer = [CollisionID.Enemies],
            mask = [CollisionID.Players, CollisionID.Projectiles, CollisionID.Enemies, CollisionID.Farm]
        ))

        self.init_Entity()