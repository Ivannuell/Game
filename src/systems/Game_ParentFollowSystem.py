import math

from components.components import *
from entities.player import Player
from systems.system import System


class ParentFollowSystem(System):
    def update(self, entities, dt):
        for e in entities:
            if e.has(Parent, OffsetPosition, Position):
                # print(e)
                parent = e.get(Parent).entity
                if not parent.has(Position, Health):
                    continue
                parent_pos = parent.get(Position)
                offset = e.get(OffsetPosition)
                pos = e.get(Position)

                x = offset.x
                y = offset.y

                if parent.has(Rotation):
                    parent_rot = parent.get(Rotation)
                    angle = parent.get(Rotation).rad_angle
                    cos_a = math.cos(angle)
                    sin_a = math.sin(angle)

                    rx = x * cos_a - y * sin_a
                    ry = x * sin_a + y * cos_a
                    
                    if not e.has(AutoCannon):
                        e.get(Rotation).rad_angle = parent_rot.rad_angle
                        
                else:
                    rx, ry = x, y

                pos.x = parent_pos.x + rx 
                pos.y = parent_pos.y + ry
