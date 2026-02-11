import pygame
from UI.Widgets.widget import Widget
from UI.uiStyle import UIStyle
from types import FunctionType


class Button(Widget):
    def __init__(self, menu, pos, size, style: UIStyle, on_click: FunctionType, text=None):
        super().__init__(menu)
        self.rect = pygame.Rect(*pos, *size)
        self.on_click = on_click
        self.style = style
        self.text = text

    def draw(self, screen):
        text = self.style.font.render(f"{self.text}", False, 'White')

        pygame.draw.rect(screen, self.style.bg_color, self.rect, self.style.border_width)
        screen.blit(text, self.rect.topleft)
    
    def update(self, dt):
        return super().update(dt)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if not self.on_click is None:
                self.on_click()
                
