from components.components import *
from entities.entity import Entity
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene

class HealthBar_DisplaySystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)


    def render(self, entities: list[Entity], screen):
        BAR_WIDTH = 20
        BAR_HEIGHT = 1
        Y_OFFSET = 4  # space below entity

        for e in entities:
            if e.has(Farm):
                continue
            if not e.has(Health, ViewPosition, Collider):
                continue

            pos = e.get(ViewPosition)
            col = e.get(Collider)
            health = e.get(Health)

            # Clamp health percent
            percent = max(0.0, min(health.health / health.max_health, 1.0))

            x = pos.x - BAR_WIDTH / 2
            y = pos.y + col.height / 2 + Y_OFFSET

            back_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
            fill_rect = pygame.Rect(x, y, BAR_WIDTH * percent, BAR_HEIGHT)

            pygame.draw.rect(screen.display_surface, (255, 0, 0), back_rect, 1)
            pygame.draw.rect(screen.display_surface, (0, 255, 0), fill_rect)


