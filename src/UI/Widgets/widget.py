from abc import ABC, abstractmethod


class Widget(ABC):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu


    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass


