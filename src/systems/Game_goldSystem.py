from typing import TYPE_CHECKING

from entities.player import Player
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene

from components.components import Destroy, EarnGoldEvent, GoldContainer
from systems.system import System


class Earn_GoldSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt: float):
        player: Player | None = None

        for entity in entities:
            if entity.has(GoldContainer):
                player = entity
                break

        if player is None:
            return
        
        for entity in entities:
            if entity.has(EarnGoldEvent):
                entity.add(Destroy())
                container = player.get(GoldContainer)
                gold_earned = entity.get(EarnGoldEvent).amount

                container.gold += gold_earned




            
