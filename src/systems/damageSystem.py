from typing import TYPE_CHECKING
from systems.system import System

if TYPE_CHECKING:
    from entities.entity import Entity


class DamageSystem(System):


    def update(self, entities: list["Entity"], dt):
        damagers: list[Entity] = []
        damagables: list[Entity] = []


        for entity in entities:
            if entity.has_component("Health"):
                damagables.append(entity)

            if entity.has_component("Damage") and entity.has_component("CollidedWith"):
                damagers.append(entity)

        for damager in damagers:
            others = damager.get_component("CollidedWith").entities
            damage = damager.get_component("Damage").damage

            for other in others:
                for damageble in damagables:
                    if damageble in others:
                        damageble.get_component("Health").health -= damage

        
