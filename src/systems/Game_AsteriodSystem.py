from typing import TYPE_CHECKING

import pygame

from components.components import *
from entities.asteriods import Asteriod
from registries.EntityConfigs import Asteriod1
from systems.system import System


if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene



class Asteriods_ManagementSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities, dt):
        farmDestroyed = []

        for e in entities: 
            if e.has(FarmDestroyed):
              farmDestroyed.append(e)  

        for e in entities:
            if not e.has(ZoneComponent):
                continue

            zone = e.get(ZoneComponent)
            for events in farmDestroyed:
                event = events.get(FarmDestroyed)
                if event.id == zone.id:
                    zone.count -= 1
                    events.add(Destroy())
                
            
        


class Asteriod_ZoneSystem(System):
    def __init__(self, scene):
        super().__init__(scene)


    def render(self, entities: 'list[Entity]', screen):
        for e in entities:
            if not e.has(ZoneComponent):
                continue

            zone = e.get(ZoneComponent)

            pygame.draw.rect(screen.display_surface, 'yellow', self.create_rect(zone.pos, zone.size), 1)


    def create_rect(self, pos, size):
        camera = self.scene.camera
        screen_center = self.scene.game.screen.display_surface.get_rect().center

        dx = pos[0] - camera.x
        dy = pos[1] - camera.y

        pos_x = dx * camera.zoom + screen_center[0]
        pos_y = dy * camera.zoom + screen_center[1]
        
        rect = pygame.Rect(0, 0,  size[0], size[1])
        rect.center = (pos_x, pos_y)
        rect.scale_by_ip(camera.zoom)

        return rect