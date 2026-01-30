from typing import TYPE_CHECKING
from systems.system import System
from components.components import *

if TYPE_CHECKING:
    from entities.entity import Entity


class DamageSystem(System):
    def __init__(self, scene) -> None:
        super().__init__(scene)

    def update(self, entities: list["Entity"], dt):
        damagables: list[Entity] = []

        for entity in entities:
            if entity.has(Health, DamageEvent):
                damagables.append(entity)

        for entity in damagables:
            source = entity.get(DamageEvent)

            if source.source.get(FactionIdentity).faction != entity.get(FactionIdentity).faction:
                entity.get(Health).health -= source.amount
                entity.add(HitBy(source.source))

                entity.remove(DamageEvent)


        
