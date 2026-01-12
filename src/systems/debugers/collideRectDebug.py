import math
import pygame
from components.components import Component
from entities.entity import Entity
from systems.system import System
from components.components import *

def draw_forward_debug(surface, position, rotation, length=40, color=(0, 255, 0)):
    angle = rotation.rad_angle

    end = (
        position.x + math.cos(angle) * length,
        position.y - math.sin(angle) * length
    )

    pygame.draw.line(
        surface,
        color,
        (position.x, position.y),
        end,
        2
    )


class DebugCollisionRenderSystem(System):
    def __init__(self, enabled=False,):
        super().__init__()
        self.enabled = enabled

    def render(self, entities: list[Entity], screen):
        colliders = []
        
        if not self.enabled:
            return

        camera: Zoom
        for e in entities:
            if e.has(Zoom):
                camera = e.get(Zoom)
            
            if e.has(ViewPosition, Position, Collider):
                colliders.append(e)

        for e in colliders:
            viewpos = e.get(ViewPosition)
            col = e.get(Collider)
            screen_center = screen.display_surface.get_rect().center

            if col.width is None or col.height is None:
                continue

            if camera.zoom is None:
                continue

            image: pygame.Surface = e.get(Sprite).image

            rect = image.get_rect()

            rect.w = col.width * camera.zoom
            rect.h = col.height * camera.zoom
            rect.center = (viewpos.x * camera.zoom + screen_center[0], 
                           viewpos.y * camera.zoom + screen_center[1] + 200)
                

            # red outline
            pygame.draw.rect(
                screen.display_surface,
                (255, 0, 0),
                rect,
                width=1
            )

        



