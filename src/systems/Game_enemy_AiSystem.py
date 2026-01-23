

import math
from turtle import position

from Utils.helper import ENEMY_ACCELARATION, move_towards, point_towards

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.enemy import Enemy
    from entities.entity import Entity
    from scenes.scene import Scene
    from scenes.play import PlayScene

from components.components import *
from systems.system import System


class Enemy_AI_MovementSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)


    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(EnemyIntent, MovementIntent, Position, Velocity):
                pos = entity.get(Position)
                rotation = entity.get(Rotation)
                vel = entity.get(Velocity)

                targetx = math.cos(rotation.angle) * vel.speed
                targety = math.sin(rotation.angle) * vel.speed

                vel.x = move_towards(vel.x, targetx, ENEMY_ACCELARATION)
                vel.y = move_towards(vel.y, targety, ENEMY_ACCELARATION)

                pos.x += vel.x * dt
                pos.y += vel.y * dt


class Enemy_AI_ShootingSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(EnemyIntent, ShootIntent, Position):
                entity.get(ShootIntent).fired = True
                

class GridIndexSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.player_grid = scene.player_grid
        self.enemy_grid = scene.enemy_grid

    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if not e.has(FactionIdentity, Position, Collider):
                continue

            faction = e.get(FactionIdentity).faction
            pos = e.get(Position)
            col = e.get(Collider)

            if faction == "ENEMY":
                self.enemy_grid.insert(e, pos, col)
            elif faction == "PLAYER":
                self.player_grid.insert(e, pos, col)


class AI_PerceptionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.enemy_grid = scene.enemy_grid
        self.player_grid = scene.player_grid
        self.frame_index = 0

    def update(self, entities: 'list[Entity]', dt: float):
        self.frame_index += 1

        for i, e in enumerate(entities):
            if not e.has(Position, Vision, Perception, FactionIdentity, Target):
                continue

            # Time slicing (1/5 per frame)
            if i % 5 != self.frame_index % 5:
                continue

            self.update_perception(e)

    def update_perception(self, entity: 'Entity'):
        pos = entity.get(Position)
        faction = entity.get(FactionIdentity).faction
        vision = entity.get(Vision)
        perception = entity.get(Perception)

        perception.entities.clear()

        if faction == "ENEMY":
            candidates = self.player_grid.query_range(pos.x, pos.y, vision.range)
        else:
            candidates = self.enemy_grid.query_range(pos.x, pos.y, vision.range)

        for target in candidates:
            if self.narrowphase_check(entity, target):
                perception.entities.append(target)


    def narrowphase_check(self, e, target):
        pos = e.get(Position)
        tpos = target.get(Position)
        vision = e.get(Vision)

        dx = tpos.x - pos.x
        dy = tpos.y - pos.y

        # print(dx*dx + dy*dy)
        # print(vision.range * vision.range)

        if dx*dx + dy*dy > (vision.range*50) * (vision.range*50):
            return False

        # FOV check (optional)
        # if not in_fov(e, target): return False

        # LOS check (optional, expensive)
        # if not has_line_of_sight(e, target): return False

        return True

            
class AI_DecisionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)

    def update(self, entities, dt):
        for e in entities:
            if not e.has(Perception, Target):
                continue

            perception = e.get(Perception)
            target = e.get(Target)

            if perception.entities:
                target.target = perception.entities[0]
            else:
                target.target = target.Main_target

            
class Enemy_AI_TargetSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for e in entities: 
            if not e.has(EnemyIntent, Target, Rotation):
                continue

            curr_target = e.get(Target).target.get(Position)
            rot = e.get(Rotation)
            pos = e.get(Position)

            rot.angle = point_towards(pos, curr_target)




        







            

''''
Enemy_AI_SpatialIndexSystem -> Creaates a grid where Players are
Enemy_AI_AwarenessSystem -> Enemy looks for the closest player
                    1. For all enemies check the grid
                    2. Base on enemy's range check all players
                    3. 
Enemy_AI_ActionSystem -> 

'''





