


from abc import abstractmethod, ABC


class Scene(ABC):
    def __init__(self, game) -> None:
        self.entities = []
        self.systems = []
        self.game = game
    
    @abstractmethod
    def on_Enter(self):
        pass

    @abstractmethod
    def on_Exit(self):
        pass

    def update(self, dt):
        for system in self.systems:
            if hasattr(system, "update"):
                system.update(self.entities, dt)

    def draw(self, screen):
        for system in self.systems:
            if hasattr(system, "render"):
                system.render(self.entities)
        
