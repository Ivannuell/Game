import pygame
from components.components import Component
from entities.entity import Entity
from systems.system import System
from components.components import *

class DebugCollisionRenderSystem(System):
    def __init__(self, enabled=True):
        self.enabled = enabled

    def render(self, entities: list[Entity], screen):
        if not self.enabled:
            return

        for e in entities:
            if not e.has(Position) or not e.has(Collider):
                continue

            pos = e.get(Position)
            col = e.get(Collider)

            rect = pygame.Rect(
                pos.x,
                pos.y,
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
