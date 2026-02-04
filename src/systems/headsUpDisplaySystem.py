


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
        game_screen = scene.game.screen.display_surface
        game_screen_rect = game_screen.get_rect()
        
        self.tiny_font = pygame.font.Font(None, 20)
        self.health_bar_con = pygame.Rect(30, game_screen_rect.height - 50, 300, 20)
        self.health_bar = self.health_bar_con.copy()
        self.health_bar_con.size = (self.health_bar_con.width + 3, self.health_bar_con.height + 3)
        self.health_bar_con.y -= 1.5

        self.health_con = self.health_bar_con.width / 100

    def render(self, entities: 'list[Entity]', screen):
        if self.player is None:
            self.player = self.scene.player_Entity
            return
        
        total_gold = self.player.get(GoldContainer).gold
        gold_text = font.render(f"GOLD: {total_gold}", False, 'yellow')
        
        screen.display_surface.blit(gold_text, (screen.width - 130, 0))

        for entity in entities:
            if entity.has(HeadQuarter) and not entity.has(EnemyIntent):

                if not entity.get(FactionIdentity).faction == "PLAYER":
                    continue

                health = entity.get(Health)

                self.health_bar.width = self.health_con * (health.health / 100) * 10

                health_text = self.tiny_font.render(f"{health.health}/{health.max_health}", False, 'white')
                pygame.draw.rect(screen.display_surface, 'red', self.health_bar, 0, 5)
                pygame.draw.rect(screen.display_surface, 'white', self.health_bar_con, 1, 5)
                screen.display_surface.blit(health_text, (self.health_bar_con.x + 20, self.health_bar_con.y - 10))


