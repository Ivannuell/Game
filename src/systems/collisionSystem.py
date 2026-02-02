from math import e
from turtle import Vec2D
import pygame

from components.components import *
from entities.asteriods import Asteriod
from entities.enemy import Enemy
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene

collision_pairs = {
    ("PLAYER", "ENEMY"),
    ("ENEMY", "PLAYER"),
    ("ENEMY", "ENEMY"),

    ("PROJECTILE", "PLAYER"),
    ("PLAYER", "PROJECTILE"),

    ("PROJECTILE", "ENEMY"),
    ("ENEMY", "PROJECTILE"),

    ("PROJECTILE", "PLAYERPART"),
    ("PLAYERPART", "PROJECTILE"),

    ("PROJECTILE", "FARM"),
    ("FARM", "PROJECTILE"),

    ("PLAYER", "BASE"),
    ("BASE", "PLAYER"),
    ("PLAYER", "FARM"),
    ("FARM", "PLAYER"),

    ("ENEMY", "FARM"),
    ("FARM", "ENEMY")
}


class CollisionSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)
        self.rect_cache = {}

    def update(self, entities: list['Entity'], dt):
        colliders = []
        self.rect_cache = {}
        # self.scene.collision_grid.cells = {}

        for e in entities:
            if e.has(Collider, GridCell):
                colliders.append(e)

            if e.has(CollidedWith):
                e.get(CollidedWith).entities.clear()

        
        for e in colliders:
            pos = e.get(Position)
            col = e.get(Collider)
            grid_cells = e.get(GridCell)


            new_cells = self.scene.collision_grid.compute_cells(pos, col)
            grid_cells = e.get(GridCell)
       

            if grid_cells.cell is None:
                self.scene.collision_grid.insert_cells(e, new_cells)
                grid_cells.cell = new_cells
            elif new_cells != grid_cells.cell:
                self.scene.collision_grid.remove_cells(e, grid_cells.cell)
                self.scene.collision_grid.insert_cells(e, new_cells)
                grid_cells.cell = new_cells


        dynamic = []
        for e in colliders:
            if e.has(Velocity):
                dynamic.append(e)


        checked = set()
        for e in dynamic:
            pos = e.get(Position)
            for other in self.scene.collision_grid.query_neighbors(pos.x, pos.y):
                if e is other:
                    continue

                pair = tuple(sorted((id(e), id(other))))
                if pair in checked:
                    continue
                checked.add(pair)

                if not other.has(Position, Collider, CollisionIdentity, FactionIdentity):
                    continue

                pos1 = e.get(Position)
                col1 = e.get(Collider)
                cid1 = e.get(CollisionIdentity)
                vel1 = e.get(Velocity)


                pos2 = other.get(Position)
                col2 = other.get(Collider)
                cid2 = other.get(CollisionIdentity)
                faction2 = other.get(FactionIdentity).faction

                # if faction1 == faction2:    
                #     continue

                if not self.can_collide(cid1, cid2):
                    continue

                if not self.is_valid_pair(cid1.role, cid2.role):
                    continue

                if not self.rects_collide(e, pos1, col1, other, pos2, col2):
                    continue

                # --- RESOLUTION DECISION ---
                if other.has(Velocity):
                    vel2 = other.get(Velocity)
                    self.resolve_dynamic_dynamic(
                        e, other,
                        pos1, vel1, col1,
                        pos2, vel2, col2
                    )
                else:
                    self.resolve_dynamic_static(
                        e, other,
                        pos1, vel1, col1,
                        pos2, col2
                    )

                self.register_colliders(e, other)


    @staticmethod
    def can_collide(a, b):
        return (
            any(m in b.layer for m in a.mask)
            and
            any(m in a.layer for m in b.mask)
        )

    @staticmethod
    # @lru_cache
    def make_rect(pos, collider):
        return pygame.Rect(
            pos.x - collider.width / 2,
            pos.y - collider.height / 2,
            collider.width,
            collider.height
        )

    @staticmethod
    def is_valid_pair(e1, e2):
        return (e1, e2) in collision_pairs

    def get_rect(self, e, pos1, col1) -> pygame.Rect:
        if e not in self.rect_cache:
            self.rect_cache[e] = self.make_rect(pos1, col1)
        return self.rect_cache[e]

    def register_colliders(self, e1, e2):
        e1.get(CollidedWith).entities.append(e2)
        e2.get(CollidedWith).entities.append(e1)
    

    def rects_collide(self, e1, p1, c1, e2, p2, c2):
        r1 = self.get_rect(e1, p1, c1)
        r2 = self.get_rect(e2, p2, c2)

        return r1.colliderect(r2)

    def resolve_dynamic_static(self, e1, e2, pos1, vel1, col1, pos2, col2):
        r1 = self.get_rect(e1, pos1, col1)
        r2 = self.get_rect(e2, pos2, col2)

        overlap_x = min(r1.right, r2.right) - max(r1.left, r2.left)
        overlap_y = min(r1.bottom, r2.bottom) - max(r1.top, r2.top)

        if overlap_x <= 0 or overlap_y <= 0:
            return

        if overlap_x < overlap_y:
            if r1.centerx < r2.centerx:
                pos1.x -= overlap_x
            else:
                pos1.x += overlap_x
            if vel1.x > 0: vel1.x = 0
        else:
            if r1.centery < r2.centery:
                pos1.y -= overlap_y
            else:
                pos1.y += overlap_y
            if vel1.y > 0: vel1.y = 0


    def resolve_dynamic_dynamic(self,e1, e2, p1, v1, c1, p2, v2, c2):
        bounce = -1

        r1 = self.get_rect(e1, p1, c1)
        r2 = self.get_rect(e2, p2, c2)

        # penetration depths
        dx = min(r1.right - r2.left, r2.right - r1.left)
        dy = min(r1.bottom - r2.top, r2.bottom - r1.top)

        # split correction
        half_dx = dx / 2
        half_dy = dy / 2

        if dx < dy:
            if r1.centerx < r2.centerx:
                p1.x -= half_dx
                p2.x += half_dx
            else:
                p1.x += half_dx
                p2.x -= half_dx

            copy_x1 = v1.x
            copy_x2 = v2.x

            v1.x *= bounce
            v2.x *= bounce
            # v1.x = (copy_x2 * bounce) 
            # v2.x = (copy_x1 * bounce)

            # v1.x = clamp_value(v1.x, max(v1.x, v2.x), 100)
            # v2.x = clamp_value(v2.x, max(v1.x, v2.x), 100)
        else:
            if r1.centery < r2.centery:
                p1.y -= half_dy
                p2.y += half_dy
            else:
                p1.y += half_dy
                p2.y -= half_dy

            copy_y1 = v1.y
            copy_y2 = v2.y

            v1.y *= bounce
            v2.y *= bounce
            # v1.y = (copy_y2 * -1)
            # v2.y = (copy_y1 * -1) 

            # v1.y = clamp_value(v1.y, max(v1.y, v2.y), 100)
            # v2.y = clamp_value(v2.y, max(v1.y, v2.y), 100)
