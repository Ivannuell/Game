from typing import TYPE_CHECKING

from entities.player import Player
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene

from components.components import *
from systems.system import System


class Earn_GoldSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt: float):
        has_goldContainers = []
        gold_events = []

        for entity in entities:
            if entity.has(GoldContainer):
                has_goldContainers.append(entity)

            if entity.has(EarnGoldEvent):
                gold_events.append(entity)
        
        for earnGold in gold_events:
            for entity in has_goldContainers:
                event = earnGold.get(EarnGoldEvent)
                source = event.source
                amount = event.amount

                if source.has(Parent):
                    source = source.get(Parent).entity

                if source is entity:
                    source.get(GoldContainer).gold += amount
                    earnGold.add(Destroy())






            
