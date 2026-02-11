import pygame


class Menu:
    def __init__(self, rect=(0,0,300, 100)):
        self.surface = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        self.pos = (rect[0], rect[1])
        self.visible = False
        self.widgets = []

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, dt):
        if not self.visible:
            return
        for w in self.widgets:
            w.update(dt)

    def handle_event(self, events):
        if not self.visible:
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
        if not self.visible:
            return
        
        self.surface.fill((0,0,0,0))

        for w in self.widgets:
            w.draw(self.surface)

        screen.display_surface.blit(self.surface, self.pos)
