


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene

from components.components import Destroy, GridCell, IsDead
from systems.system import System


class CleanupSystem(System):
    def update(self, entities, dt):
        for e in entities:
            if not e.has(Destroy):
                continue

            if e.has(GridCell):
                self.scene._grid.remove(e, e.get(GridCell).cells)

            self.scene.entity_manager.remove(e)











class _CleanupSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        entities[:] = [e for e in entities if not e.has(Destroy)]
