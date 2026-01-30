

import math
import random
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
        self.asteriod_grid = scene.asteriod_grid

    def update(self, entities: 'list[Entity]', dt):
        self.enemy_grid.entity_count = 0
        self.player_grid.entity_count = 0
        self.asteriod_grid.entity_count = 0

        for e in entities:
            if not e.has(FactionIdentity, Position, Collider):
                continue

            faction = e.get(FactionIdentity).faction
            pos = e.get(Position)
            col = e.get(Collider)

            if faction == "ENEMY":
                self.enemy_grid.insert(e, pos, col)
                self.enemy_grid.entity_count += 1
            elif faction == "PLAYER":
                self.player_grid.insert(e, pos, col)
                self.player_grid.entity_count += 1
            elif faction == "FARM":
                self.asteriod_grid.insert(e, pos, col)
                self.asteriod_grid.entity_count += 1


class AI_PerceptionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.enemy_grid = scene.enemy_grid
        self.player_grid = scene.player_grid
        self.asteriod_grid = scene.asteriod_grid
        self.frame_index = 0
        self.time = 0

    def update(self, entities: 'list[Entity]', dt: float):
        self.frame_index += 1
        
        for i, e in enumerate(entities):
            if not e.has(Position, Vision, Perception, FactionIdentity, Target):
                continue

            perception = e.get(Perception)
            target = e.get(Target)

            # Time slice: 1/5 of entities per frame
            if i % 10 != self.frame_index % 10:
                continue

            perception.cooldown -= dt
            if perception.cooldown > 0:
                continue

            if target.target is not target.prev_target:
                continue

            self.update_perception(e)
            perception.cooldown = random.randint(1, 2) * 0.1

    def update_perception(self, entity: 'Entity'):
        pos = entity.get(Position)
        vision = entity.get(Vision)
        perception = entity.get(Perception)

        perception.visible_entities.clear()

        if entity.has(Attacker):
            candidates = self.player_grid.query_range(pos.x, pos.y, vision.range)
        elif entity.has(Farmer):
            candidates = self.asteriod_grid.query_range(pos.x, pos.y, vision.range)
        else:
            candidates = self.enemy_grid.query_range(pos.x, pos.y, vision.range)

        for target in candidates:
            if self.narrowphase_check(entity, target):
                perception.visible_entities.append(target)
                if len(perception.visible_entities) >= 3:
                    continue

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

    def update(self, entities: 'list[Entity]', dt):
        def distance(pos1, pos2):
            dx = pos1.x - pos2.x
            dy = pos1.y - pos2.y

            return dx*dx + dy*dy
        
            
        for e in entities:
            if not e.has(Perception, Target, Attacker):
                continue
            target = e.get(Target)
            visisble_Entities = e.get(Perception).visible_entities

            target.prev_target = target.target

            if target.Main_target.has(IsDead):
                if visisble_Entities:
                    target.Main_target = visisble_Entities[0]
                e.get(Velocity).speed = 0

            elif visisble_Entities:
                target.target = visisble_Entities[0]
                e.get(Velocity).speed = 50

            else:
                target.target = target.Main_target

                

        

            
class Enemy_AI_TargetSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.time = 0

    def update(self, entities: 'list[Entity]', dt):
        self.time += dt
        if self.time > 0.3:
            self.time = 0
            return 
        

        for e in entities: 
            if not e.has(EnemyIntent, Target, Rotation, Velocity):
                continue
            
            target_comp = e.get(Target)
            rot = e.get(Rotation)
            pos = e.get(Position)

            # def is_dead(ent):
            #     return ent is None or ent.has(IsDead)

            # # --- Target resolution ---
            # if is_dead(main_target):

            #     if nearby:
            #         # Retarget to nearest visible entity
            #         target_comp.prev_target = main_target
            #         target_comp.target = nearby[0]

            #     else:
            #         # No targets available → stop
            #         target_comp.target = None
            #         velocity.speed = 0
            #         return  # nothing to aim at

            # --- At this point, target is guaranteed valid ---
            curr_target = target_comp.target.get(Position)

            # Rotate toward target
            rot.angle = point_towards(pos, curr_target)




        







            

''''
Enemy_AI_SpatialIndexSystem -> Creaates a grid where Players are
Enemy_AI_AwarenessSystem -> Enemy looks for the closest player
                    1. For all enemies check the grid
                    2. Base on enemy's range check all players
                    3. 
Enemy_AI_ActionSystem -> 

'''





