
from entities.entity import Entity

from components.components import *
from scenes.scene import Scene


class Player(Entity):
    def __init__(self, scene: Scene, config: dict = {}, ):
        super().__init__(scene)

        self.__qualname__ = "Player"

        self.add(Animation(
            spritesheet=config["Sprite"],
            animation = config["Anim"]
        ))
        self.add(AnimationState())
        self.add(Position(config["Pos"][0], config["Pos"][1]))
        self.add(Velocity(config["Vel"]))
        self.add(Size(48,48))
        self.add(Sprite())
        self.add(MovementIntent())
        self.add(Collider())
        self.add(InputControlled())
        self.add(ShootIntent())
        self.add(FactionIdentity("PLAYER"))
        self.add(CollisionIdentity(
            role="PLAYER",
            layer = [CollisionID.Players], 
            mask = [CollisionID.Enemies, CollisionID.Obstacles, CollisionID.Farm] 
        ))

        self.add(CollidedWith())
        self.add(Health(500))
        self.add(Rotation())
        self.add(ViewPosition())

        self.add(GoldContainer(1000))

        self.init_Entity()