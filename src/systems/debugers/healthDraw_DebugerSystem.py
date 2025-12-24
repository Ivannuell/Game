from entities.entity import Entity
import pygame
from systems.system import System
from components.components import *

class HealthDraw(System):
    def __init__(self) -> None:
        super().__init__()

    def render(self, entities: list[Entity], screen):
        font = pygame.font.Font(None, 20)

        for entity in entities:
            if entity.has(Health) and entity.has(Position):
                health = entity.get(Health).health
                position = entity.get(Position)

                text = font.render(f"Health: {health}", False, "white")
                textRect = text.get_rect()

                textRect.bottomleft = (position.x, position.y)

                screen.display_surface.blit(text, textRect)
            


