
import time
import pygame
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from Game_Managers.entity_Manager import EntityManager


if TYPE_CHECKING:
    from Utils.systemProfiler_overlay import DebugOverlaySystem
    from Game_Managers.assetManager import AssetsManager
    from Game_Managers.inputManager import InputManager
    from Game_Managers.scene_Manager import SceneManager
    from Utils.systemProfiler import SystemProfiler


class Scene(ABC):
    def __init__(self, game) -> None:
        self.entities = []
        self.systems = []
        self.disabledSystems = []

        self.entity_manager = EntityManager(self.entities)
        self.game = game
        self.asset_manager: 'AssetsManager' = game.asset_manager
        self.input_manager: 'InputManager' = game.input_manager
        self.profiler: 'SystemProfiler' = game.profiler
        self.profiler_overlay: 'DebugOverlaySystem' = game.profiler_overlay
    
    @abstractmethod
    def on_Create(self):
        pass

    def on_Enter(self):
        pass

    def on_Exit(self):
        pass

    def on_Pause(self):
        pass

    def on_Resume(self):
        pass

    def handle_input(self, events):
        self.input_manager.begin_frame()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            self.input_manager.process_event(event)


    def update(self, dt):
        for system in self.systems:
            if not system.Enabled:
                continue

            if hasattr(system, "update"):
                start = time.perf_counter()
                system.update(self.entities, dt)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                self.profiler.record(system.__class__.__name__, elapsed)
        
        self.entity_manager.commit()

    def render(self, screen):
        for system in self.systems:
            if not system.Enabled:
                continue

            if hasattr(system, "render"):
                start = time.perf_counter()
                system.render(self.entities, screen)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                self.profiler.record(system.__class__.__name__, elapsed)

    @property
    def blocks_input(self) -> bool:
        return True
    
    @property
    def blocks_update(self) -> bool:
        return True
        
