from systems.system import System
from components.components import *
from entities.entity import Entity

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.scene import Scene

class HealthSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: list["Entity"], dt):
        events = []

        for entity in entities:

            if not entity.has(Health):
                continue

            health = entity.get(Health).health
            if health <= 0:
                if entity.has(EnemyIntent, Gold):
                    gold = entity.get(Gold).amount

                    earn_gold = Entity(self.scene)
                    earn_gold.add(EarnGoldEvent(gold))
                    events.append(earn_gold)

                entity.add(Destroy())


            if entity.has(Parent):
                if entity.get(Parent).entity.has(Destroy):
                    entity.add(Destroy())

        entities.extend(events)



            