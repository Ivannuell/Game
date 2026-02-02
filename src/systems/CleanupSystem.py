


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


from components.components import Destroy, IsDead
from systems.system import System


class CleanupSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        entities[:] = [e for e in entities if not e.has(Destroy)]



