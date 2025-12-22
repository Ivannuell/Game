import pygame
from entities.entity import Entity
from systems.system import System

class DebugCollisionRenderSystem(System):
    def __init__(self, enabled=True):
        self.enabled = enabled

    def render(self, entities: list[Entity], screen):
        if not self.enabled:
            return

        for e in entities:
            if not e.has_component("Position") or not e.has_component("Collider"):
                continue

            pos = e.get_component("Position")
            col = e.get_component("Collider")

            rect = pygame.Rect(
                pos.x + col.offset_x,
                pos.y + col.offset_y,
                col.width,
                col.height
            )

            # red outline
            pygame.draw.rect(
                screen.display_surface,
                (255, 0, 0),
                rect,
                width=1
            )
