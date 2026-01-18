import math
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene
    
from systems.system import System
from components.components import *


class WorldRenderSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def render(self, entities: 'list[Entity]', screen):
        visibles = []
        camera: Zoom
        for e in entities:
            if e.has(Zoom):
                camera = e.get(Zoom)

            if e.has(Sprite, ViewPosition):
                visibles.append(e)


        for e in visibles: 
            image = e.get(Sprite).image
            view = e.get(ViewPosition)

            if e.has(Rotation):
                rot = e.get(Rotation)
                image = pygame.transform.rotate(image, rot.visual_deg)

            image = pygame.transform.scale_by(image, camera.zoom)
            screen_center = screen.display_surface.get_rect().center

            screen_x = view.x * camera.zoom + screen_center[0]
            screen_y = view.y * camera.zoom + screen_center[1]

            rect = image.get_rect(center=(screen_x, screen_y))
            screen.display_surface.blit(image, rect)



