from entities.entity import Entity
from components.components import *
from registries.AnimationStateList import AnimationMode

class Base(Entity):
    def __init__(self, scene):
        super().__init__(scene)
        self.__qualname__ = "Base"

        self.add(Animation(
            spritesheet="ship",
            animation = {
                "ship-idle": Anim([], [(0,0,48,48)], 0, 0.2, AnimationMode.LOOP)
            }
        ))
        self.add(CollisionIdentity(
            role="BASE",
            layer = [CollisionID.Obstacles],
            mask = [CollisionID.Players]
            
        ))
        self.add(CollidedWith())
        self.add(Position(270, 480))
        self.add(Sprite())
        self.add(Size(48,48, 4))
        self.add(Collider())
        self.add(Static())
        self.add(FactionIdentity("BASE"))
        self.add(Rotation())
        self.add(ViewPosition())
        self.add(HeadQuarter())
        self.add(Health(1000))

        self.init_Entity()