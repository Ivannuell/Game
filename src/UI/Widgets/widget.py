from abc import ABC, abstractmethod


class Widget(ABC):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self._children = []
        self._parent = None

    def update(self, dt):
        self.update_self(dt)
    
        if self._children:
            for child in self._children:
                child.update(dt)

    def draw(self, screen):
        self.draw_self(screen)
    
        if self._children:
            for child in self._children:
                child.draw(screen)

    def on_show(self, payload):
        for child in reversed(self._children):
            child.on_show(payload)

        self.on_show(payload)


    @abstractmethod
    def handle_self_event(self, event) -> bool:
        return True
    
    @abstractmethod
    def draw_self(self, screen):
        pass

    @abstractmethod
    def update_self(self, dt):
        pass

    def handle_event(self, event) -> bool:
        if self._children:
            for child in reversed(self._children):
                if child.handle_event(event):
                    return True

        return self.handle_self_event(event)
