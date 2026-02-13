from icecream import ic
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
        self.text = self.style.font.render(f"{text}", False, 'White')

    def draw_self(self, screen):
        pygame.draw.rect(screen, self.style.bg_color, self.rect, self.style.border_width)
        screen.blit(self.text, (self.rect.centerx - self.text.width/2, self.rect.centery - self.text.height/2))
    
    def update_self(self, dt):
        pass
    
    def handle_self_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if not self.on_click is None:
                self.on_click()
                return True
        return False