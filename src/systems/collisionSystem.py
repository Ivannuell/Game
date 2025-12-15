import pygame
from entities.entity import Entity

class CollisionSystem:
    def __init__(self):
        pass

    def update(self, entities: list[Entity], dt):
        static_colliders = []
        dynamic_colliders = []

        for e in entities:
            pos = e.get_component("Position")
            col = e.get_component("Collider")

            has_velocity = e.has_component("Velocity")
            is_solid = e.has_component("Solid")

            if has_velocity:
                dynamic_colliders.append(e)
            elif is_solid:
                static_colliders.append(e)

        for dyn in dynamic_colliders:
            for stat in static_colliders:
                if dyn is stat:
                    continue

                if self.rects_collide(dyn, stat):
                    self.resolve_dynamic_static(dyn, stat)


    

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
