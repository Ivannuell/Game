from entities.entity import Entity
import pygame
from systems.system import System
from components.components import *

class HealthDraw(System):
    def __init__(self, Projectiles=False, Entity=False) -> None:
        super().__init__()
        self.Projectiles = Projectiles
        self.Entity = Entity

    def render(self, entities: list[Entity], screen):
        font = pygame.font.Font(None, 20)
        projectiles = []
        collection = []

        
        for entity in entities:
            if entity.has(Projectile):
                projectiles.append(entity)

            if entity.has(Health, Position, FactionIdentity):
                collection.append(entity)
        if self.Projectiles:
            for entity in collection:
                health = entity.get(Health).health
                position = entity.get(Position)
                faction = entity.get(FactionIdentity).faction

                text = font.render(f"Health: {health} \nFaction: {faction}", False, "white")
                textRect = text.get_rect()

                textRect.bottomleft = (position.x, position.y)

                screen.display_surface.blit(text, textRect)

        if self.Entity:
            for proj in projectiles:
                faction = proj.get(FactionIdentity).faction
                pos = proj.get(Position)

                text = font.render(f"Faction: {faction}", False, "white")
                textRect = text.get_rect()

                textRect.bottomleft = (pos.x, pos.y)

                screen.display_surface.blit(text, textRect)
            


