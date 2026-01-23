import math

from components.components import *
from entities.player import Player
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


class ParentFollowSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if e.has(Parent, OffsetPosition, Position):
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
                    angle = parent.get(Rotation).angle
                    cos_a = math.cos(angle)
                    sin_a = math.sin(angle)

                    rx = x * cos_a - y * sin_a
                    ry = x * sin_a + y * cos_a
                    
                    if not e.has(Cannon):
                        e.get(Rotation).angle = parent_rot.angle
                        
                else:
                    rx, ry = x, y

                pos.x = parent_pos.x + rx 
                pos.y = parent_pos.y + ry
