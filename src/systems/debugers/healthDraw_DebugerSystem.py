from entities.entity import Entity
import pygame

class HealthDraw:
    def __init__(self, screen):
        self.screen = screen

    def update(self, entities: list[Entity], dt):
        font = pygame.font.Font(None, 20)

        for entity in entities:
            if entity.has_component("Health") and entity.has_component("Position"):
                health = entity.get_component("Health").health
                position = entity.get_component("Position")

                text = font.render(f"Health: {health}", False, "white")
                textRect = text.get_rect()

                textRect.bottomleft = (position.x, position.y)

                self.screen.display_surface.blit(text, textRect)
            


