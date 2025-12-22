from typing import TYPE_CHECKING
from systems.system import System
from components.components import *

if TYPE_CHECKING:
    from entities.entity import Entity


class DamageSystem(System):


    def update(self, entities: list["Entity"], dt):
        damagers: list[Entity] = []
        damagables: list[Entity] = []


        for entity in entities:
            if entity.has(Health):
                damagables.append(entity)

            if entity.has(Damage) and entity.has(CollidedWith):
                damagers.append(entity)

        for damager in damagers:
            others = damager.get(CollidedWith).entities
            damage = damager.get(Damage).damage

            for other in others:
                for damageble in damagables:
                    if damageble in others:
                        damageble.get(Health).health -= damage

        
