import pygame 
from screen import Screen
from entities.entity import Entity

class RenderSystem:
    def __init__(self, screen: Screen):
        self.screen = screen

    def render(self, entities: list[Entity]):
        for entity in entities:
            try:
                sprite = entity.get_component('Sprite')
                position = entity.get_component('Position')
            except:
                continue

            self.screen.display_surface.blit(sprite.image, (position.x, position.y))

