import pygame
from UI.uiStyle import UIStyle

pygame.font.init()


INVENTORY_STYLE = UIStyle(
    bg_color=(40, 40, 40),
    border_color=(120, 120, 120),
    hover_color=(80, 80, 80),
    text_color=(220, 220, 220)
)

SHOP_STYLE = UIStyle(
    bg_color=(60, 40, 20),
    border_color=(180, 140, 60),
    hover_color=(100, 70, 30),
    text_color=(255, 220, 160),
    border_width=0,
    font=pygame.Font(None, 20)
)
