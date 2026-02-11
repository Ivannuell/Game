import pygame
from UI.Widgets.widget import Widget
from UI.uiStyle import UIStyle


class Button(Widget):
    def __init__(self, menu, pos, size, style: UIStyle, on_click):
        super().__init__(menu)
        self.rect = pygame.Rect(*pos, *size)
        self.on_click = on_click
        self.style = style

    def draw(self, screen):
        pygame.draw.rect(screen, self.style.bg_color, self.rect, self.style.border_width)
    
    def update(self, dt):
        return super().update(dt)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            print("Pressed")
            self.on_click()
                
