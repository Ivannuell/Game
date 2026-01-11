from components.components import *
from entities.entity import Entity


class CameraEntity(Entity):

    def __init__(self, game):
        super().__init__(game)
        self.alive = True
        self.add(Zoom())
        self.add(SystemEntity())
