from icecream import ic
import pygame


class Menu:
    def __init__(self, pos=(0,0), size=(100,100)):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.size = size
        self.pos = pos
        self._visible = False
        self.widgets = []
        self.context = None

    def show(self, payload):
        self._visible = True
        self.context = payload
        self.on_show()

    def on_show(self):
        pass

    def hide(self):
        self._visible = False

    def update(self, dt):
        if not self._visible:
            return
        for w in self.widgets:
            w.update(dt)

    def handle_event(self, events):
        if not self._visible:
            return 
        
        for event in events:
            if hasattr(event, "pos"):
                event.pos = (
                    event.pos[0] - self.pos[0],
                    event.pos[1] - self.pos[1]
                )

            for widget in self.widgets:
                widget.handle_event(event)

    def draw(self, screen):
        if not self._visible:
            return
        
        self.surface.fill((0,0,0,0))

        for w in self.widgets:
            w.draw(self.surface)

        screen.display_surface.blit(self.surface, self.pos)
