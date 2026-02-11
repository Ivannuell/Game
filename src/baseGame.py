from typing import TYPE_CHECKING

from Game_Managers.UI_Manager import UIManager
from Game_Managers.assetManager import AssetsManager
from Game_Managers.command_Manager import CommandManager
from Game_Managers.inputManager import InputManager
from UI.Menus.pauseMenu import Pause_Menu
from Utils.systemProfiler import SystemProfiler
from Utils.systemProfiler_overlay import DebugOverlaySystem

if TYPE_CHECKING:
    from screen import Screen

    
import pygame
from Game_Managers.scene_Manager import SceneManager
from registries.SceneList import SceneList



class BaseGame:
    def __init__(self):
        self.screen: "Screen | None" = None
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.fps = 60.0
    
        self.asset_manager: AssetsManager = AssetsManager()
        self.input_manager: InputManager = InputManager()
        self.ui_manager = UIManager()

        self.profiler = SystemProfiler()
        self.profiler_overlay = DebugOverlaySystem(self.profiler)
        
        self.scene_manager = SceneManager(self)
        self.command_manager = CommandManager(self.scene_manager)
        
    def set_screen(self, screen: "Screen"):
        if self.screen:
            del self.screen
            self.screen = None
        self.screen = screen

        if self.screen:
            self.screen.show()


    def start(self):
        self.scene_manager.push(SceneList.PRELOAD)

        self.ui_manager.register('pause', Pause_Menu(self.ui_manager, self.command_manager, (200, 200, 300, 500)))
        
        while True:
            self.delta_time = self.clock.tick(self.fps) / 1000
            events = pygame.event.get()

            self.scene_manager.handle_input(events)
            self.ui_manager.handle_event(events)
            
            self.scene_manager.update(self.delta_time)
            self.ui_manager.update(self.delta_time)

            self.scene_manager.render(self.screen)
            self.ui_manager.draw(self.screen)

            self.command_manager.flush()

            self.profiler_overlay.update()
            self.profiler_overlay.render(self.screen.display_surface) # type: ignore

            if self.screen is not None: self.screen.draw()