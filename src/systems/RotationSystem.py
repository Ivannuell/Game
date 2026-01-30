import math
from components.components import Rotation
from entities.player import Player
from entities.playerPart import PlayerPart
from Utils.helper import ROTATION_SMOOTHNESS, SPRITE_FORWARD_OFFSET, lerp_angle
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


class RotationSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if e.has(Rotation):
                rot = e.get(Rotation)

                rot.angleOfAttack = -math.degrees(
                    rot.angle - SPRITE_FORWARD_OFFSET - self.scene.camera.rotation
                )

                rot.angle += rot.angular_vel * dt
                rot.angular_vel *= 0.85  # damping

                # interpolate
                t = 1 - math.exp(-ROTATION_SMOOTHNESS * dt)
                rot.visual_deg = lerp_angle(rot.visual_deg, rot.angleOfAttack, t)
                rot.visual_deg = round(rot.visual_deg, 5)

