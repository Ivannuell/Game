from components.components import *
from entities.entity import Entity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.scene import Scene


class CameraEntity(Entity):

    def __init__(self, scene: 'Scene'):
        super().__init__(scene)
        self.alive = True
        self.add(Zoom())
        self.add(UtilityEntity())
