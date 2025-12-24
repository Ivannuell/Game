from turtle import width
import pygame
from typing import TYPE_CHECKING
from scenes.game import GameScene

if TYPE_CHECKING:
    from entities.entity import Entity

from components.components import Clickable, Position, Size
from systems.system import System
pygame.font.init()

font = pygame.Font(None, 50)

class ButtonDisplaySystem(System):
    def render(self, entities: list['Entity'], screen):
        for entity in entities:
           if entity.has(Clickable):
                size = entity.get(Size)
                pos = entity.get(Position)
                clickable = entity.get(Clickable)

                rect = pygame.Rect(pos.x, pos.y, size.width, size.height)

                if clickable.buttonID == "PLAY":
                    pygame.draw.rect(screen.display_surface, 'green', rect)
                    text = font.render("PLAY GAME", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))
                if clickable.buttonID == "EXIT":
                    pygame.draw.rect(screen.display_surface, 'white', rect)
                    text = font.render("EXIT", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))
                if clickable.buttonID == "RESUME":
                    pygame.draw.rect(screen.display_surface, 'yellow', rect)
                    text = font.render("EXIT", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))
