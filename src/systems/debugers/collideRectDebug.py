import pygame
from entities.entity import Entity

class DebugCollisionRenderSystem:
    def __init__(self, screen, enabled=True):
        self.screen = screen
        self.enabled = enabled

    def update(self, entities: list[Entity], dt):
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
                self.screen.display_surface,
                (255, 0, 0),
                rect,
                width=1
            )
