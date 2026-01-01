import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from screen import Screen

from entities.system_Entities.camera import CameraEntity
from systems.system import System
from components.components import *


class WorldRenderSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def render(self, entities, screen):
        visibles = []
        camera: Zoom


        for e in entities:
            if e.has(Zoom):
                camera = e.get(Zoom)

            if e.has(Sprite, ViewPosition, Position):
                visibles.append(e)
                



        for e in visibles: 
            sprite = e.get(Sprite)
            view = e.get(ViewPosition)

            image = sprite.image

            if e.has(Rotation):
                image = pygame.transform.rotate(
                    image,
                    -math.degrees(e.get(Rotation).rad_angle - self.game.camera.rotation)
                )

            image = pygame.transform.scale_by(image, camera.zoom)
            screen_center = screen.display_surface.get_rect().center

            screen_x = view.x * camera.zoom + screen_center[0]
            screen_y = view.y * camera.zoom + screen_center[1] + 200

            rect = image.get_rect(center=(screen_x, screen_y))


            # rect = image.get_rect(center=(view.x, view.y))
            screen.display_surface.blit(image, rect)


