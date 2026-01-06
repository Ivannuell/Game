from components.components import *
from entities.entity import Entity


class CameraEntity(Entity):

    def __init__(self):
        super().__init__()
        self.alive = True
        self.add(Zoom())
        self.add(SystemEntity())
