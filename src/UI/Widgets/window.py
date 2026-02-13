


import pygame
from UI.Widgets.widget import Widget


class Window(Widget):
    def __init__(self, menu):
        super().__init__(menu)

    def draw_self(self, screen):
        pygame.draw.rect(screen, (255,255,255,128), screen.get_rect())
    
    def update_self(self, dt):
        pass
    
    def handle_self_event(self, event):
        return False