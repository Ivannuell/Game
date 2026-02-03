

import math
import random
from turtle import position

from Utils.helper import ENEMY_ACCELARATION, move_towards, point_towards

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.ship import Spaceship
    from entities.entity import Entity
    from scenes.scene import Scene
    from scenes.play import PlayScene

from Utils._spatialGrid import SpatialGrid
from components.components import *
from systems.system import System


class Enemy_AI_MovementSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)


    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Bot, MovementIntent, Position, Velocity):
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
            if entity.has(Bot, ShootIntent, Position):
                entity.get(ShootIntent).fired = True
                
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
            if not e.has(Bot, Target, Rotation, Velocity):
                continue
            
            target_comp = e.get(Target)
            rot = e.get(Rotation)
            pos = e.get(Position)

            if target_comp.target is None:
                continue

            curr_target = target_comp.target.get(Position)

            rot.angle = point_towards(pos, curr_target)


class AI_AttackerDecisionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.grid = scene._grid

    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if not e.has(Attacker, Perception):
                continue

            target = e.get(Target)
            pos = e.get(Position)
            perception = e.get(Perception)
            
            perception.cooldown += dt
            if target.target is None:
                if not perception.cooldown >= perception.time:
                    continue

                perception.cooldown = 0.0
                target.target = self.grid.find_nearest(pos.x, pos.y, predicate=lambda e: 
                                                    e.has(FactionIdentity) and e.get(FactionIdentity).faction == "PLAYER")
            
            elif target.target.has(IsDead):
                target.target = None
            
         
class AI_FarmerDecisionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.grid = scene._grid

    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if e.has(Perception, Vision, Farmer, Target):
                target = e.get(Target)
                pos = e.get(Position)
                perception = e.get(Perception)

                perception.cooldown += dt
                if target.target is None:
                    if not perception.cooldown >= perception.time:
                        continue
                    
                    perception.cooldown = 0.0
                    target.target = self.grid.find_nearest(pos.x, pos.y, require_component=Farm)
                
                elif target.target.has(IsDead):
                    target.target = None
                    perception.cooldown = -random.uniform(0.0, perception.time)
           





        


class _AI_AttackerPerceptionSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)
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

        if entity.has(Farmer):
            return
        candidates = []
        perception.visible_entities.clear()
        
        if e.has(Attacker):
            for e in self.scene.collision_grid.query_range(pos.x, pos.y, vision.range):
            
                candidates.append

        for target in candidates:
            if self.narrowphase_check(entity, target):
                perception.visible_entities.append(target)

    def narrowphase_check(self, e, target):
        if e is None or target is None:
            return False
        
        pos = e.get(Position)
        tpos = target.get(Position)
        vision = e.get(Vision)

        dx = tpos.x - pos.x
        dy = tpos.y - pos.y

        if dx*dx + dy*dy > (vision.range*50) * (vision.range*50):
            return False

        # FOV check (optional)
        # if not in_fov(e, target): return False

        # LOS check (optional, expensive)
        # if not has_line_of_sight(e, target): return False

        return True

            
class _AI_AttackerDecisionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):

        for e in entities:
            if not e.has(Perception, Target, Attacker):
                continue
            target = e.get(Target)
            all_visible_Entities = e.get(Perception).visible_entities

            visible_Entities = [e for e in all_visible_Entities if e.has(Attacker)]

            target.prev_target = target.target

            if target.Main_target.has(IsDead):
                if visible_Entities:
                    target.Main_target = visible_Entities[0]
                e.get(Velocity).speed = 0

            elif visible_Entities:
                target.target = visible_Entities[0]
                e.get(Velocity).speed = 50

            else:
                target.target = target.Main_target






            

''''
Enemy_AI_SpatialIndexSystem -> Creaates a grid where Players are
Enemy_AI_AwarenessSystem -> Enemy looks for the closest player
                    1. For all enemies check the grid
                    2. Base on enemy's range check all players
                    3. 
Enemy_AI_ActionSystem -> 

'''





