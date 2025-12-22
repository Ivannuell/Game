

import pygame
from abc import abstractmethod, ABC


class Scene(ABC):
    def __init__(self, game) -> None:
        self.entities = []
        self.systems = []
        self.game = game
    
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
            if hasattr(system, "update"):
                system.update(self.entities, dt)

    def render(self, screen):
        for system in self.systems:
            if hasattr(system, "render"):
                system.render(self.entities, screen)

    @property
    def blocks_input(self) -> bool:
        return True
    @property
    def blocks_update(self) -> bool:
        return True
        
