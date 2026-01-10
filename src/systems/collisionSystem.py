from math import e
from turtle import Vec2D
import pygame

from components.components import *
from spatialGrid import SpatialGrid
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

collision_pairs = {
    ("PLAYER", "ENEMY"),
    ("ENEMY", "PLAYER"),

    ("PROJECTILE", "PLAYER"),
    ("PLAYER", "PROJECTILE"),

    ("PROJECTILE", "ENEMY"),
    ("ENEMY", "PROJECTILE"),

    ("PROJECTILE", "PLAYERPART"),
    ("PLAYERPART", "PROJECTILE"),
}


class CollisionSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.grid = game.grid

        self.rect_cache = {}

        self.dyn_rects = []
        self.stat_rects = []

    def update(self, entities: list['Entity'], dt):
        static_colliders = []
        dynamic_colliders = []
        self.dyn_rects = []
        self.stat_rects = []
        self.rect_cache = {}
        self.grid.clear()

        for e in entities:
            if e.has(Collider) and not e.has(Velocity):
                static_colliders.append(e)
            else:
                dynamic_colliders.append(e)

            if e.has(CollidedWith):
                e.get(CollidedWith).entities.clear()


        self.dyn_rects = [
            [e,
             e.get(Position),
             e.get(Velocity),
             e.get(Collider),
             e.get(CollisionIdentity),
             e.get(FactionIdentity).faction]
            for e in dynamic_colliders
            if e.has(Position, Velocity, Collider, CollisionIdentity, FactionIdentity)]
        
        for e in self.dyn_rects:
            pos = e[1]
            col = e[3]
            self.grid.insert(e[0], pos, col)


        checked = set()

        for e1, pos1, vel1, col1, cid1, faction1 in self.dyn_rects:
            for other in self.grid.query_neighbors(pos1.x ,pos1.y):
                if e1 is other:
                    continue

                pair = tuple(sorted((id(e1), id(other))))
                if pair in checked:
                    continue
                checked.add(pair)

                if not other.has(Position, Velocity, Collider, CollisionIdentity, FactionIdentity):
                    continue

                pos2 = other.get(Position)
                vel2 = other.get(Velocity)
                col2 = other.get(Collider)
                cid2 = other.get(CollisionIdentity)
                faction2 = other.get(FactionIdentity).faction

                if faction1 == faction2:
                    continue

                if not self.can_collide(cid1, cid2):
                    continue

                if not self.is_valid_pair(cid1.role, cid2.role):
                    continue

                if self.rects_collide(e1, pos1, col1, other, pos2, col2):
                    self.register_colliders(e1, other)
                    self.resolve_dynamic_dynamic(pos1, vel1, col1, pos2, vel2, col2)


    @staticmethod
    def can_collide(a, b):
        return (
            any(m in b.layer for m in a.mask)
            and
            any(m in a.layer for m in b.mask)
        )

    @staticmethod
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

    def resolve_dynamic_static(self, dyn: 'Entity', stat: 'Entity'):
        pos = dyn.get(Position)
        vel = dyn.get(Velocity)

        p1 = dyn.get(Position)
        c1 = dyn.get(Collider)
        p2 = stat.get(Position)
        c2 = stat.get(Collider)

        r1 = self.make_rect(p1, c1)
        r2 = self.make_rect(p2, c2)

        dx = min(r1.right - r2.left, r2.right - r1.left)
        dy = min(r1.bottom - r2.top, r2.bottom - r1.top)

        if dx < dy:
            if r1.centerx < r2.centerx:
                pos.x -= dx
            else:
                pos.x += dx
            vel.x *= -1
        else:
            if r1.centery < r2.centery:
                pos.y -= dy
            else:
                pos.y += dy
            vel.y *= -1

    def resolve_dynamic_dynamic(self, p1, v1, c1, p2, v2, c2):
        r1 = self.make_rect(p1, c1)
        r2 = self.make_rect(p2, c2)

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

            v1.x = (copy_x2 * -1) / 3
            v2.x = (copy_x1 * -1) / 3

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

            v1.y = (copy_y2 * -1) / 3
            v2.y = (copy_y1 * -1) / 3

            # v1.y = clamp_value(v1.y, max(v1.y, v2.y), 100)
            # v2.y = clamp_value(v2.y, max(v1.y, v2.y), 100)
