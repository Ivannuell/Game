import math
from components.components import *
from components.intents import Play_CollisionImpact_Event
from entities.projectile_related.projectile import ProjectilePool
from systems.system import System
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene
    from scenes.play import PlayScene


class ProjectileSystem(System):
    def __init__(self, scene: 'PlayScene'):
        super().__init__(scene)
        self.zoom = 1
        self.center =  (scene.game.screen.display_surface.width /2, scene.game.screen.display_surface.height /2 + 500)
        self.sprite = scene.asset_manager.get_asset('projectile')

    def update(self, entites, dt):
        for p in self.scene.proj_pool.pool: # type: ignore
            if not p.alive:
                continue

            # Move
            dx = p.vx * dt
            dy = p.vy * dt
            p.x += dx
            p.y += dy
            p.range_left -= abs(dx) + abs(dy)

            if p.range_left <= 0:
                p.alive = False
                continue

            # Collision (narrow target set)
            for target in self.scene.collision_grid.query_point(p.x, p.y):
                if target.get(FactionIdentity).faction == p.faction:
                    continue

                if self.hit(p, target):
                    self.on_hit(p, target)
                    p.alive = False
                    break

    def hit(self, p, target):
        pos = target.get(Position)
        col = target.get(Collider)

        return (
            abs(p.x - pos.x) <= col.width * 0.5 and
            abs(p.y - pos.y) <= col.height * 0.5
        )

    def on_hit(self, projectile, target_entity):
        target_entity.add(DamageEvent(
            amount=projectile.damage,
            source=projectile.faction
        ))

        target_entity.add(Play_CollisionImpact_Event(projectile.x, projectile.y))

    def render(self, entities, screen):
        for e in entities:
            if e.has(Zoom):
                self.zoom = e.get(Zoom).zoom
                break


        cos_r = math.cos(-self.scene.camera.rotation) 
        sin_r = math.sin(-self.scene.camera.rotation) 
        zoomed_sprite = pygame.transform.scale_by(self.sprite, self.zoom) 

        hw = self.sprite.get_width() * 0.5
        hh = self.sprite.get_height() * 0.5
        
        for p in self.scene.proj_pool.pool:
            if p.alive:
                dx = p.x - self.scene.camera.x
                dy = p.y - self.scene.camera.y

                cam_x = dx * cos_r - dy * sin_r
                cam_y = dx * sin_r + dy * cos_r

                screen_x = cam_x * self.zoom + self.center[0]
                screen_y = cam_y * self.zoom + self.center[1] - 500

                screen.display_surface.blit(zoomed_sprite, (screen_x - hw, screen_y - hh))

