


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


from components.components import Destroy, Projectile
from systems.system import System


class CleanupSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        entities[:] = [e for e in entities if not e.has(Destroy)]




