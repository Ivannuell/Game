from typing import TYPE_CHECKING

from components.UI_Components import *

if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


import pygame
from systems.system import System

from components.components import Clickable, Position, Size

pygame.font.init()
font = pygame.Font(None, 50)

class FloatingWindow_System(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def render(self, entities: 'list[Entity]', screen):
        for e in entities:
            if not e.has(Window):
                continue

            if not e.get(Window).displaying:
                continue

            pos = e.get(Position)
            size = e.get(Size)

            transparent_surf = pygame.Surface((300, 300), pygame.SRCALPHA)

            pygame.draw.rect(transparent_surf, (255,255,255,128), (0, 0, size.width, size.height))

            screen.display_surface.blit(transparent_surf, (pos.x, pos.y))

            buttons = e.get(Buttons).buttons

            for button in buttons:
                pos = button.get(Position)

                # pos.x +=

                self.scene.entity_manager.add(button)