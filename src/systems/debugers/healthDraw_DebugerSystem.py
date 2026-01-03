from entities.entity import Entity
import pygame
from systems.system import System
from components.components import *

class HealthDraw(System):
    def __init__(self, Projectiles=False, Entity=False, Orbit=False) -> None:
        super().__init__()
        self.Projectiles = Projectiles
        self.Entity = Entity
        self.Orbit = Orbit

    def render(self, entities: list[Entity], screen):
        font = pygame.font.Font(None, 20)
        projectiles = []
        collection = []

        
        for entity in entities:
            if entity.has(Projectile):
                projectiles.append(entity)

            if entity.has(Health, Position, FactionIdentity):
                collection.append(entity)

            if entity.has(Orbit):
                if self.Orbit:
                    pos = entity.get(Orbit).center.get(ViewPosition)
                    size = entity.get(Orbit).center.get(Size)
                    pygame.draw.circle(screen.display_surface, "green", (pos.x, pos.y), 5)
                    pygame.draw.circle(screen.display_surface, "yellow", (pos.x, pos.y), entity.get(Orbit).radius, 1)


        if self.Entity:
            for entity in collection:
                health = entity.get(Health).health
                position = entity.get(ViewPosition)
                faction = entity.get(FactionIdentity).faction

                text = font.render(f"Health: {health} \nFaction: {faction}", False, "white")
                textRect = text.get_rect()

                textRect.bottomleft = (position.x + screen.display_surface.get_width() / 2, position.y + screen.display_surface.get_height() / 2 + 200)

                screen.display_surface.blit(text, textRect)

        if self.Projectiles:
            for proj in projectiles:
                faction = proj.get(FactionIdentity).faction
                pos = proj.get(ViewPosition)

                text = font.render(f"Faction: {faction}", False, "white")
                textRect = text.get_rect()

                textRect.bottomleft = (pos.x, pos.y)

                screen.display_surface.blit(text, textRect)
            


