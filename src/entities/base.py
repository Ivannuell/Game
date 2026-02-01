from entities.entity import Entity
from components.components import *
from registries.AnimationStateList import AnimationMode

class Base(Entity):
    def __init__(self, scene, config={}):
        super().__init__(scene)
        self.__qualname__ = "Base"

        self.add(Animation(
            spritesheet=config["Spritesheet"],
            animation =config["Animation"]
        ))
        self.add(Position(*config["Position"]))
        self.add(Size(*config["Size"]))
        self.add(FactionIdentity(config["Faction"]))



        self.add(CollisionIdentity(
            role="BASE",
            layer = [CollisionID.Obstacles],
            mask = [CollisionID.Players]
        ))
        self.add(CollidedWith())
        self.add(Sprite())
        self.add(Collider())
        self.add(Static())
        self.add(Rotation())
        self.add(ViewPosition())
        self.add(HeadQuarter())
        self.add(Health(1000))

        self.add(GoldContainer(10000))
        self.add(GridCell())

        self.init_Entity()