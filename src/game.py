import pygame
from sys import exit
from screen import Screen
from assetManager import AssetsManager
from inputManager import InputManager

from systems.AnimationSystem import AnimationSystem
from systems.RenderSystem import RenderSystem
from entities.player import Player
from scenes.scene import Scene
from scenes.game import GameScene

class BaseGame:
    def __init__(self):
        self.screen: Screen | None = None
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.fps = 60

        self.player: Player
        self.animation: AnimationSystem
        self.renderSys: RenderSystem

        self.current_scene: Scene = GameScene(self)
        
        self.asset_manager = AssetsManager()
        self.input_manager = InputManager()
        
    def set_screen(self, screen: Screen):
        if self.screen:
            del self.screen
            self.screen = None

        self.screen = screen

        if self.screen:
            self.screen.show()

        self.initialize()

    def initialize(self):
        self.asset_manager.load_assets()

        self.current_scene.on_Enter()


    def start(self):
        while True:
            self.delta_time = self.clock.tick(self.fps) / 1000

            self.events()
            self.update()
            self.render()

    def update(self):
        self.current_scene.update(self.delta_time)

    def render(self):
        self.current_scene.draw(self.screen)

        self.screen.draw()

    def events(self):
        self.input_manager.begin_frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            self.input_manager.process_event(event)
