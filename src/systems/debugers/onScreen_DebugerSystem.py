
from typing import TYPE_CHECKING
import pygame
from systems.system import System

if TYPE_CHECKING:
    from entities.entity import Entity


class OnScreenDebugSystem(System):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.font = pygame.font.Font(None, 20)
        self.timer = 0
        self.debug = self.font.render(f"FPS: 0", False, "white")

    def render(self, entities: list["Entity"], screen):
        # posx, posy = self.game.camera.x, self.game.camera.y
        # posx, posy = 0,0

        # pygame.draw.aalines(self.game.screen.display_surface, "green", False, [
        #                   (posx, posy), 
        #                   (posx + self.game.screen.display_surface.get_width()/2, posy), 
        #                   (posx + self.game.screen.display_surface.get_width()/2, posy + self.game.screen.display_surface.get_height()/2),
        #                   (posx, posy + self.game.screen.display_surface.get_height()/2),
        #                   (posx, posy)
        #                   ])

        fps = round(self.game.clock.get_fps(), 2)

        if self.timer >= 1:
            self.debug = self.font.render(f"FPS: {fps}", False, "white")
            self.timer = 0

        screen.display_surface.blit(self.debug, (10, 10))
        self.timer += self.game.delta_time
