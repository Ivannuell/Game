
from typing import TYPE_CHECKING
import pygame
from systems.system import System

if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


class OnScreenDebugSystem(System):
    def __init__(self, scene: 'Scene'):
        super().__init__(scene)
        self.font = pygame.font.Font(None, 20)
        self.timer = 0
        self.debug = self.font.render(f"FPS: 0", False, "white")
        self.debug_time = self.font.render(f"frame Time: 0.0", False, "white")

    def render(self, entities: list["Entity"], screen):
        fps = round(self.scene.game.clock.get_fps(), 2)

        if self.timer >= 1:
            self.debug = self.font.render(f"FPS: {fps}", False, "white")
            self.debug_time = self.font.render(f"frame Time: {self.scene.game.delta_time}", False, "white")
            self.timer = 0

        screen.display_surface.blit(self.debug, (10, 10))
        screen.display_surface.blit(self.debug_time, (10, 30))
        self.timer += self.scene.game.delta_time
