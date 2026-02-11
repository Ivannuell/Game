


import pygame
from UI.Widgets.widget import Widget


class Window(Widget):
    def __init__(self, menu):
        super().__init__(menu)

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255,128), screen.get_rect())
        
    
    def update(self, dt):
        return super().update(dt)
    
    def handle_event(self, event):
        return super().handle_event(event)