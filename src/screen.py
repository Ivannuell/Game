import pygame
import spritesheet

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.display_surface: "pygame.surface.Surface"

    def show(self):
        self.display_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('SpriteAction')

        print('Screen Added')

    def draw(self):
        pygame.display.update()
        
        self.display_surface.fill('black')