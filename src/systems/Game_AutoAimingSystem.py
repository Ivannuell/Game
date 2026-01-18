


import pygame
from components.components import *
from Utils.spatialGrid import SpatialGrid
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene


"""
    1. Create a range grid using SpatialGrid class and take the Global projectile pool
    2. Makes sure that grid is empty
    3. takes All entity that has Auto Aiming Cannons if non taken return
    4. Takes all the enemies and insert them to the Grid
    5. For all all cannons take their info.
        5.1 - for every enemy that is inside the range
        5.2 - set the current angle of that cannon facing to the enemy
"""

class AutoAimingSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)
        self.enemy_inRange_grid = SpatialGrid(50)

    def update(self, entities: 'list[Entity]', dt):
        self.enemy_inRange_grid.clear()
        self.auto_cannons = []

        for e in entities:
            if e.has(AutoCannon):
                self.auto_cannons.append(e)

        if len(self.auto_cannons) <= 0:
            return

        for e in entities:
            if e.has(EnemyIntent):
                pos = e.get(Position)
                col = e.get(Collider)

                self.enemy_inRange_grid.insert(e, pos, col)
        
        
        for cannon in self.auto_cannons:
            cannon_pos = cannon.get(Position)
            cannon_range = cannon.get(AutoCannon)
            cannon_rot = cannon.get(Rotation)
            cannon_intent = cannon.get(ShootIntent)
            enemy_inRange = []

            for enemy in self.enemy_inRange_grid.query_range(
                    cannon_pos.x, cannon_pos.y, cannon_range.range):

                enemy_pos = enemy.get(Position)

                dx = enemy_pos.x - cannon_pos.x
                dy = enemy_pos.y - cannon_pos.y
                distance = dx*dx + dy*dy

                enemy_inRange.append((enemy, distance))

            if not enemy_inRange:
                continue

            enemy_inRange.sort(key=lambda e: e[1])
            enemy = enemy_inRange[0]

            enemy_pos = enemy[0].get(Position)

            dx = enemy_pos.x - cannon_pos.x
            dy = enemy_pos.y - cannon_pos.y
            cannon_rot.rad_angle = math.atan2(dy, dx)

            cannon_intent.fired = True


            
        
