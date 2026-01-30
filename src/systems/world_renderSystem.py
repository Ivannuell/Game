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
        Camera_View = self.scene.camera

        for e in entities:
            if e.has(Sprite, ViewPosition):
                visibles.append(e)


        for e in visibles: 
            image = e.get(Sprite).image
            view = e.get(ViewPosition)
            
            if not screen.display_surface.get_rect().collidepoint((view.x, view.y)):
                continue

            if e.has(Rotation):
                rot = e.get(Rotation)
                image = pygame.transform.rotate(image, rot.visual_deg)

            image = self.scale_image(image, Camera_View.zoom)

            rect = image.get_rect(center=(view.x, view.y))
            screen.display_surface.blit(image, rect)

    @lru_cache
    def scale_image(self, image, zoom):
        return pygame.transform.scale_by(image, zoom)


