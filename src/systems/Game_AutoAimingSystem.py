


import pygame
from components.components import *
from entities.entity import Entity
from spatialGrid import SpatialGrid
from systems.system import System



class AutoAimingSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.range_grid = SpatialGrid(50)
        self.projectiles = game.proj_pool

    def update(self, entities: list[Entity], dt):
        self.range_grid.clear()
        cannon_pos = (0,0)
        cannon: Entity | None = None

        for e in entities:
            if e.has(AutoCannon):
                cannon = e
                cannon_pos = (e.get(Position).x, e.get(Position).y)

        for e in entities:
            if e.has(EnemyIntent):
                pos = e.get(Position)
                col = e.get(Collider)

                self.range_grid.insert(e, pos, col)
        
        if cannon is None:
            return
        
        cannon.get(AutoCannon).time_left += dt

        for enemy in self.range_grid.query_range(cannon_pos[0], cannon_pos[1], 10):
            # print(enemy)
            enemy_pos = enemy.get(Position)
            cannon_rot = cannon.get(Rotation)
            cannon_can = cannon.get(AutoCannon)



            # cannon_rot.rad_angle = math.radians(pygame.Vector2(cannon_pos[0], cannon_pos[1]).angle_to((enemy_pos.x, enemy_pos.y)) + 45)
            # cannon_rot.angular_vel = 2

            dx = enemy_pos.x - cannon_pos[0]
            dy = enemy_pos.y - cannon_pos[1]

            cannon_rot.rad_angle = math.atan2(dy, dx)

            if cannon_can.time_left >= cannon_can.cooldown:
                self.projectiles.spawn(
                    x=cannon_pos[0],
                    y=cannon_pos[1],
                    vx=math.cos(cannon_rot.rad_angle) * 900,
                    vy=math.sin(cannon_rot.rad_angle) * 900,
                    faction="PLAYER",
                    damage=20,
                    max_range=1200
                )            
                cannon_can.time_left = 0
            break

            
        
