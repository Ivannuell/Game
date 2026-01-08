from components.components import Rotation
from entities.player import Player
from systems.system import System


class RotationSystem(System):
    def update(self, entities, dt):
        for e in entities:
            if e.has(Rotation):

                r = e.get(Rotation)
                r.rad_angle += (r.target_angle - r.rad_angle) * r.smoothing * dt

