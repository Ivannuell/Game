import pygame
from UI.Widgets.widget import Widget


class Label(Widget):
    def __init__(self, menu, pos, size, text, style):
        super().__init__(menu)
        self.x, self.y = pos
        self.width, self.height = size
        self.context = text
        self.text = style.font.render(self.context, False, 'black')
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_self(self, screen):
        screen.blit(self.text, self.rect)
    
    def update_self(self, dt):
        pass
    
    def handle_self_event(self, event):
        return False
