


from typing import TYPE_CHECKING

import pygame

from components.components import *
from entities.player import Player
from systems.system import System

if TYPE_CHECKING:
    from scenes.scene import Scene
    from entities.entity import Entity

# pygame.font.F

pygame.font.init()
font = pygame.font.Font(None, 30)    


class HeadsUpDisplaySystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)
        self.player: Player = scene.player_Entity

    def render(self, entities: 'list[Entity]', screen):
        if self.player is None:
            self.player = self.scene.player_Entity
            return
        
        total_gold = self.player.get(GoldContainer).gold
        gold_text = font.render(f"GOLD: {total_gold}", False, 'yellow')
        
        screen.display_surface.blit(gold_text, (screen.width - 130, 0))


