import math
from components.components import Rotation
from entities.player import Player
from entities.playerPart import PlayerPart
from helper import ROTATION_SMOOTHNESS, SPRITE_FORWARD_OFFSET, lerp_angle
from systems.system import System


class RotationSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def update(self, entities, dt):
        for e in entities:
            if e.has(Rotation):
                rot = e.get(Rotation)

                target_deg = -math.degrees(
                    rot.rad_angle - SPRITE_FORWARD_OFFSET - self.game.camera.rotation
                )

                rot.rad_angle += rot.angular_vel * dt
                rot.angular_vel *= 0.85  # damping

                # interpolate
                t = 1 - math.exp(-ROTATION_SMOOTHNESS * dt)
                rot.visual_deg = lerp_angle(rot.visual_deg, target_deg, t)

