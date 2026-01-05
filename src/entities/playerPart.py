from entities.entity import Entity

from components.components import *


class PlayerPart(Entity):
    def __init__(self, config):
        super().__init__()

        self.add(Position(0, 0))
        self.add(ViewPosition())
        self.add(Parent())
        self.add(OffsetPosition())
        self.add(Size(48, 48))
        self.add(InputControlled())
        self.add(Solid())
        self.add(Collider())
        self.add(Velocity(config["Vel"]))
        self.add(Sprite())
        self.add(Animation(
            spritesheet=config["Sprite"],
            animation=config["Anim"]
        ))
        self.add(AnimationState())
        self.add(FactionIdentity("PLAYER"))
        self.add(CollisionIdentity(
            layer=[CollisionID.Players],
            mask=[CollisionID.Enemies, CollisionID.Projectiles]
        ))
        # self.add(Rotation())
                   