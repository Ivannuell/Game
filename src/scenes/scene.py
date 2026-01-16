

import time
import pygame
from abc import abstractmethod, ABC


class Scene(ABC):
    def __init__(self, game) -> None:
        self.entities = []
        self.systems = []
        self.game = game
        self.disabledSystems = []
    
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
        self.game.input_manager.begin_frame()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            self.game.input_manager.process_event(event)


    def update(self, dt):
        for system in self.systems:
            if not system.Enabled:
                continue

            if hasattr(system, "update"):
                start = time.perf_counter()
                system.update(self.entities, dt)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                self.game.profiler.record(system.__class__.__name__, elapsed)

    def render(self, screen):
        for system in self.systems:
            if not system.Enabled:
                continue

            if hasattr(system, "render"):
                start = time.perf_counter()
                system.render(self.entities, screen)
                elapsed = (time.perf_counter() - start) * 1000  # ms
                self.game.profiler.record(system.__class__.__name__, elapsed)

    @property
    def blocks_input(self) -> bool:
        return True
    @property
    def blocks_update(self) -> bool:
        return True
        
