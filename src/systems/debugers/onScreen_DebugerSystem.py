
from typing import TYPE_CHECKING
import pygame
if TYPE_CHECKING:
    from entities.entity import Entity


class OnScreenDebugSystem:
    def __init__(self, game):
        self.screen = game.screen
        self.game = game
        self.font = pygame.font.Font(None, 20)
        self.timer = 0
        self.debug = self.font.render(f"FPS: 0", False, "white")

    def update(self, entities: list["Entity"], dt):
        fps = round(self.game.clock.get_fps(), 2)
        
        if self.timer >= 1:
            self.debug = self.font.render(f"FPS: {fps}", False, "white")
            self.timer = 0

        self.screen.display_surface.blit(self.debug, (10,10))
        self.timer += dt