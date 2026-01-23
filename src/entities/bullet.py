import math
from warnings import deprecated
from entities.entity import Entity
from components.components import *

@deprecated("Now uses object-derived projectiles")
class Bullet(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.active = False

        self.__qualname__ = "Bullet"
        # self.add(Animation(
        #     spritesheet="bullet",
        #     animation={
        #         "bullet-idle": Anim([], [(0, 0, 6, 9)], 0, 0.2)
        #     }
        # ))
        self.add(CollisionIdentity(
            role="PROJECTILE",
            layer=[CollisionID.Projectiles],
            mask=[CollisionID.Enemies, CollisionID.Obstacles, CollisionID.Players] 

        ))
        self.add(Size(6,9))
        self.add(Sprite())
        self.add(Collider())
        self.add(Damage(50))
        self.add(ViewPosition())
        self.add(Position(0, 0))
        self.add(Projectile())
        self.add(FactionIdentity())
        self.add(Rotation())
        self.add(Velocity())
        self.add(CollidedWith())

        self.init_Entity()

    def spawn(self, shooter):
        pos = self.get(Position)
        vel = self.get(Velocity)
        proj = self.get(Projectile)
        rotation = self.get(Rotation)
        
        shooter_pos = shooter.get(Position)

        proj.reset()
        angle = shooter.get(Rotation).rad_angle

        pos.x = shooter_pos.x 
        pos.y = shooter_pos.y

        rotation.angle = angle
        self.get(FactionIdentity).faction = shooter.get(FactionIdentity).faction

        vel.speed = 900
        vel.x = math.cos(angle) * vel.speed
        vel.y = math.sin(angle) * vel.speed

        self.active = True