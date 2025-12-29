from typing import TYPE_CHECKING

from Camera import Camera
if TYPE_CHECKING:
    from screen import Screen

    
import pygame
from assetManager import AssetsManager
from inputManager import InputManager
from scenes.scene_Manager import SceneManager

from references import SceneList



class BaseGame:
    def __init__(self):
        self.screen: "Screen | None" = None
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.fps = 60

        self.scene_manager: SceneManager = SceneManager(self)
        self.asset_manager: AssetsManager = AssetsManager()
        self.input_manager: InputManager = InputManager()
        self.camera = Camera()
        
    def set_screen(self, screen: "Screen"):
        if self.screen:
            del self.screen
            self.screen = None
        self.screen = screen

        if self.screen:
            self.screen.show()

        self.initialize()

    def initialize(self):
        self.scene_manager.push(SceneList.PRELOAD)

    def start(self):
        while True:
            self.delta_time = self.clock.tick(self.fps) / 1000

            self.scene_manager.handle_input(pygame.event.get())
            self.scene_manager.update(self.delta_time)
            self.scene_manager.render(self.screen)

            if self.screen is not None: self.screen.draw()