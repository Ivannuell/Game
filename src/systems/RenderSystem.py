import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from screen import Screen

from systems.system import System
from components.components import *


class RenderSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def render(self, entities, screen):
        for e in entities:
            if not e.has(Sprite, ViewPosition, Position):
                continue

            sprite = e.get(Sprite)
            view = e.get(ViewPosition)
            pos = e.get(Position)

            image = sprite.image

            if e.has(Rotation):
                image = pygame.transform.rotate(
                    image,
                    -math.degrees(e.get(Rotation).rad_angle - self.game.camera.rotation)
                )

            rect = image.get_rect(center=(view.x, view.y))
            # rect = image.get_rect(center=(pos.x, pos.y))
            # rect = image.get_rect(topleft=(view.x, view.y))
            screen.display_surface.blit(image, rect)


