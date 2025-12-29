


import math
from components.components import *
from systems.system import System


class OrbitSystem(System):
    def update(self, entities, dt):
        for e in entities:
            if not e.has(Orbit, Position, Rotation):
                continue

            orbit = e.get(Orbit)
            pos = e.get(Position)
            rot = e.get(Rotation)
            center = orbit.center.get(Position)
            center_size = orbit.center.get(Size)

            orbit.angle += orbit.speed * dt

            # Position
            ox = math.cos(orbit.angle) * orbit.radius
            oy = math.sin(orbit.angle) * orbit.radius

            pos.x = center.x + ox
            pos.y = center.y + oy

            dx = math.sin(orbit.angle)
            dy = -math.cos(orbit.angle)

            SPRITE_FORWARD_OFFSET = -math.pi / 2  # sprite faces up
            rot.rad_angle = math.atan2(dy, dx) + SPRITE_FORWARD_OFFSET


