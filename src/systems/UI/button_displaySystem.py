from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


import pygame
from systems.system import System

from components.components import Clickable, Position, Size

pygame.font.init()
font = pygame.Font(None, 50)
tiny_font = pygame.Font(None, 20)

class ButtonDisplaySystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def render(self, entities: list['Entity'], screen):

        rect = pygame.Rect(0,0,screen.display_surface.get_width(), screen.display_surface.get_height())
        pygame.draw.rect(screen.display_surface, (0,0,0,120), rect)

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
                    text = font.render("RESUME", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))
                if clickable.buttonID == "RESTART":
                    pygame.draw.rect(screen.display_surface, 'green', rect)
                    text = font.render("RESTART", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))

                if clickable.buttonID == "PAUSE":
                    pygame.draw.rect(screen.display_surface, 'green', rect)
                    text = font.render("||", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))

                if clickable.buttonID == "HIDE":
                    pygame.draw.rect(screen.display_surface, 'green', rect)
                    text = tiny_font.render("Hide", False, 'black')
                    screen.display_surface.blit(text, (rect.centerx - text.width/2, rect.centery - text.height/2))

                
                    

