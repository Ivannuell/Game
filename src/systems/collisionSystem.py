import pygame
from entities.entity import Entity

class CollisionSystem:
    def __init__(self):
        pass

    def update(self, entities: list[Entity], dt):
        static_colliders = []
        dynamic_colliders = []

        for e in entities:
            has_velocity = e.has_component("Velocity")
            is_solid = e.has_component("Solid")
            is_parts = e.has_component("Ship")

            if has_velocity and is_parts:
                continue
            elif has_velocity:
                dynamic_colliders.append(e)
            elif is_solid:
                static_colliders.append(e)

        for dyn in dynamic_colliders:
            for stat in static_colliders:
                if dyn is stat:
                    continue

                if self.rects_collide(dyn, stat):
                    self.resolve_dynamic_static(dyn, stat)

        for i in range(len(dynamic_colliders)):
            for j in range(i + 1, len(dynamic_colliders)):
                e1 = dynamic_colliders[i]
                e2 = dynamic_colliders[j]

                if self.rects_collide(e1, e2):
                    self.resolve_dynamic_dynamic(e1, e2)
    

    def rects_collide(self, e1, e2):
        p1 = e1.get_component("Position")
        c1 = e1.get_component("Collider")
        p2 = e2.get_component("Position")
        c2 = e2.get_component("Collider")

        r1 = pygame.Rect(
            p1.x + c1.offset_x,
            p1.y + c1.offset_y,
            c1.width,
            c1.height
        )

        r2 = pygame.Rect(
            p2.x + c2.offset_x,
            p2.y + c2.offset_y,
            c2.width,
            c2.height
        )

        return r1.colliderect(r2)


    def resolve_dynamic_static(self, dyn, stat):
        pos = dyn.get_component("Position")
        vel = dyn.get_component("Velocity")

        p1 = dyn.get_component("Position")
        c1 = dyn.get_component("Collider")
        p2 = stat.get_component("Position")
        c2 = stat.get_component("Collider")

        r1 = pygame.Rect(p1.x, p1.y, c1.width, c1.height)
        r2 = pygame.Rect(p2.x, p2.y, c2.width, c2.height)

        dx = min(r1.right - r2.left, r2.right - r1.left)
        dy = min(r1.bottom - r2.top, r2.bottom - r1.top)

        if dx < dy:
            if r1.centerx < r2.centerx:
                pos.x -= dx
            else:
                pos.x += dx
            print('Collides')
            vel.x = 0
        else:
            if r1.centery < r2.centery:
                pos.y -= dy
            else:
                pos.y += dy
            vel.y = 0
            print('Collides')

    def resolve_dynamic_dynamic(self, e1, e2):
        p1 = e1.get_component("Position")
        v1 = e1.get_component("Velocity")
        c1 = e1.get_component("Collider")

        p2 = e2.get_component("Position")
        v2 = e2.get_component("Velocity")
        c2 = e2.get_component("Collider")

        r1 = pygame.Rect(
            p1.x + c1.offset_x,
            p1.y + c1.offset_y,
            c1.width,
            c1.height
        )
        r2 = pygame.Rect(
            p2.x + c2.offset_x,
            p2.y + c2.offset_y,
            c2.width,
            c2.height
        )

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

            v1.x = 0
            v2.x = 0
        else:
            if r1.centery < r2.centery:
                p1.y -= half_dy
                p2.y += half_dy
            else:
                p1.y += half_dy
                p2.y -= half_dy

            v1.y = 0
            v2.y = 0
