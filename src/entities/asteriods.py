from components.components import *
from entities.entity import Entity
from registries.EntityConfigs import EntityConfig


class Asteriod(Entity):
    def __init__(self, scene, config: EntityConfig):
        super().__init__(scene)
        
        self.add(Position(*config.Position))
        self.add(Animation(
            animation = config.Animation,
            spritesheet = config.Spritesheet
        ))
        self.add(Size(*config.Size))

        self.add(Collider())
        self.add(ViewPosition())
        self.add(Rotation())
        self.add(Sprite())
        self.add(FactionIdentity("FARM"))
        self.add(CollisionIdentity(
            role="FARM",
            layer=[CollisionID.Farm],
            mask=[CollisionID.Enemies, CollisionID.Players, CollisionID.Projectiles]
        ))
        # self.add(Velocity(10))
        self.add(CollidedWith())
        self.add(Gold(100))
        self.add(Health(200))
        self.add(GridCell())
        self.add(TargetedBy())

        self.add(Farm())

        self.init_Entity()