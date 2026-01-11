from components.components import SystemEntity
from entities.entity import Entity


class Executable(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.alive = True
        self.add(SystemEntity())