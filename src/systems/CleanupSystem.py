


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


from components.components import Destroy, Projectile
from systems.system import System


class CleanupSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        new_entities = []
    
        for entity in entities:
            if entity.has(Projectile):
                if not entity.active: # type: ignore
                    continue

            if not entity.has(Destroy):
                new_entities.append(entity)
        
        entities[:] = new_entities





