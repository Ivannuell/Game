import pygame
from components.components import Component
from entities.entity import Entity
from systems.system import System
from components.components import *

class DebugCollisionRenderSystem(System):
    def __init__(self, enabled=False):
        super().__init__()
        self.enabled = enabled

    def render(self, entities: list[Entity], screen):
        if not self.enabled:
            return

        for e in entities:
            if not e.has(Position) or not e.has(Collider):
                continue

            pos = e.get(Position)
            col = e.get(Collider)

            if col.width is None or col.height is None:
                continue

            rect = pygame.Rect(
                pos.x - col.width / 2,
                pos.y - col.height / 2,
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
