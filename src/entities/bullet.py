import math
from entities.entity import Entity
from components.components import *


class Bullet(Entity):
    def __init__(self, game):
        super().__init__()
        self.active = False

        self.__qualname__ = "Bullet"
        self.add(Animation(
            spritesheet="bullet",
            animation={
                "bullet": Anim([], [(0, 0, 6, 9)], 0, 0.2)
            }
        ))
        self.add(CollisionIdentity(
            layer=[CollisionID.Projectiles],
            # mask=[CollisionID.Enemies, CollisionID.Obstacles, CollisionID.Players]
            mask=[]

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

        self.game = game
        self.init_Entity()

    def spawn(self, shooter):
        pos = self.get(Position)
        vel = self.get(Velocity)
        proj = self.get(Projectile)
        shooter_pos = shooter.get(Position)
        rotation = self.get(Rotation)

        proj.reset()
        angle = shooter.get(Rotation).rad_angle

        pos.x = shooter_pos.x 
        pos.y = shooter_pos.y

        rotation.rad_angle = angle
        self.get(FactionIdentity).faction = shooter.get(FactionIdentity).faction

        vel.speed = 900
        vel.x = math.cos(angle) * vel.speed
        vel.y = math.sin(angle) * vel.speed

        speed = math.hypot(vel.x, vel.y)
        assert abs(speed - vel.speed) < 0.01, f"Bad velocity reset: {speed}"
        self.active = True