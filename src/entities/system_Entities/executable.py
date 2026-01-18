from components.components import SystemEntity
from entities.entity import Entity


class Executable(Entity):
    def __init__(self, scene):
        super().__init__(scene)
        self.alive = True
        self.add(SystemEntity())