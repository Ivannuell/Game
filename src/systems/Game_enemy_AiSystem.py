

import math
import random
from turtle import position

from icecream import ic

from Utils.helper import ENEMY_ACCELARATION, get_distance, move_towards, point_towards

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.spaceship import Spaceship
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
            if entity.has(Bot, MovementIntent, Position, Velocity, Target, Vision):
                pos = entity.get(Position)
                rotation = entity.get(Rotation)
                vel = entity.get(Velocity)
                target = entity.get(Target)
                vision = entity.get(Vision)

                if not target.target is None:
                    distance = get_distance(pos, target.target.get(Position))

                    if distance < (vision.range * self.scene._grid.cell_size)**2:
                        vel.speed = 0
                    else:
                        vel.speed = vel._normal_speed


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
            if entity.has(Bot, ShootIntent, Position, Target, Vision):
                target = entity.get(Target)
                if target.target is None:
                    continue

                vision = entity.get(Vision)
                pos = entity.get(Position)
                target_pos = target.target.get(Position)

                distance = get_distance(pos, target_pos)

                # ic(distance)
                # ic((vision.range * self.scene._grid.cell_size)**2)
                # print("-----")

                if distance < (vision.range * self.scene._grid.cell_size)**2:
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

    def update(self, entities, dt):
        for e in entities:
            if not e.has(Attacker, Perception, Target, Position, FactionIdentity, Vision):
                continue

            target = e.get(Target)
            pos = e.get(Position)
            perception = e.get(Perception)
            faction = e.get(FactionIdentity).faction

            perception.cooldown += dt

            # ---- Normalize dead targets ----
            main_dead = (
                target.Main_target
                and (target.Main_target.has(IsDead) or target.Main_target.has(Destroy))
            )

            curr_dead = (
                target.target
                and (target.target.has(IsDead) or target.target.has(Destroy))
            )

            # Case 1: BOTH dead → do NOTHING
            if main_dead and curr_dead:
                continue

            # Remove only the dead one
            if curr_dead:
                target.target = None

            # ---- Range check ----
            # if target.target and target.Main_target:
            #     if not (target.target.has(IsDead) or target.target.has(Destroy)):

            #         curr_pos = target.target.get(Position)
            #         dx = curr_pos.x - pos.x
            #         dy = curr_pos.y - pos.y
            #         dist_sq = dx*dx + dy*dy

            #         if dist_sq > (vision.range * self.grid.cell_size):
            #             # Prefer Main_target if it is valid
            #             if not (
            #                 target.Main_target.has(IsDead)
            #                 or target.Main_target.has(Destroy)
            #             ):
            #                 target.target = target.Main_target
            #                 continue   # 🔑 stop further processing this frame


            # ---- No retarget allowed until cooldown ----
            if target.target is None and perception.cooldown < perception.time:
                continue

            opp = "ENEMY" if faction == "PLAYER" else "PLAYER"

            # ---- Acquire / refresh target ----
            if target.target is None:
                perception.cooldown = 0.0

                # find_nearest will not stop until something is found
                found = self.grid.find_nearest(
                    pos.x, pos.y,
                    predicate=lambda ent:
                        ent.has(FactionIdentity)
                        and not ent.has(IsDead)
                        and not ent.has(Destroy)
                        and ent.get(FactionIdentity).faction == opp
                )

                if found is None:
                    perception.cooldown = -perception.time
                    continue

                target.target = found


            # ---- Compare against Main_target (if alive) ----
            if target.Main_target and not main_dead:
                main_pos = target.Main_target.get(Position)
                curr_pos = target.target.get(Position)

                dm = (main_pos.x - pos.x) ** 2 + (main_pos.y - pos.y) ** 2
                dc = (curr_pos.x - pos.x) ** 2 + (curr_pos.y - pos.y) ** 2

                if dm < dc:
                    target.target = target.Main_target
          
         
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
                    target.target = self.grid.find_nearest(pos.x, pos.y, predicate= lambda e: 
                                                           e.has(Farm, TargetedBy) 
                                                           and len(e.get(TargetedBy).entities) <= e.get(TargetedBy).maxSize)

                    targeted = target.target.get(TargetedBy)
                    targeted.entities.append(e)
                
                elif target.target.has(IsDead):
                    target.target = None
                    perception.cooldown = -random.uniform(0.0, perception.time)

           
class AI_Farmer_Gold_DecisionSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)
        self.grid = scene._grid

    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if e.has(Vision, Farmer, Target, GoldContainer, FactionIdentity):
                target = e.get(Target)
                pos = e.get(Position)
                vision = e.get(Vision)
                gold_con = e.get(GoldContainer)
                faction = e.get(FactionIdentity).faction

                base = self.scene.ally_base if faction == "PLAYER" else self.scene.enemy_base

                if gold_con.gold >= gold_con.gold_capacity:
                    target.target = base

                    if get_distance(pos, base.get(Position)) < (vision.range * self.scene._grid.cell_size) ** 2:
                        self.scene.command_manager.send("GOLD_DELIVERED", (gold_con.gold, base))
                        target.target = None
                        gold_con.gold = 0








        


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





