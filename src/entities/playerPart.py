from entities.entity import Entity

from components.components import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.scene import Scene


class PlayerPart(Entity):
    def __init__(self, scene: 'Scene', config: dict = {}):
        super().__init__(scene)

        self.add(Position(0, 0))
        self.add(ViewPosition())
        self.add(Parent())
        self.add(OffsetPosition())
        self.add(Size(48, 48))
        self.add(InputControlled())
        self.add(Collider())
        self.add(Velocity())
        # self.add(Sprite())
        # self.add(Animation(
        #     spritesheet=config["Sprite"],
        #     animation=config["Anim"]
        # ))
        # self.add(AnimationState())
        self.add(FactionIdentity("PLAYER"))
        self.add(CollisionIdentity(
            role="PLAYERPART",
            layer=[CollisionID.Players],
            mask=[CollisionID.Enemies, CollisionID.Projectiles]
        ))
        self.add(CollidedWith())
        self.add(Rotation())

        self.init_Entity()
                   