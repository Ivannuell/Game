import pygame 
from components.components import Animation
from entities.entity import Entity

class RenderSystem:
    def __init__(self, screen):
        self.screen = screen

    def render(self, entities: list[Entity]):
        for entity in entities:

            sprite = entity.get_component('Sprite')

            if not sprite:
                continue

            self.screen.display_surface.blit(sprite.image)

