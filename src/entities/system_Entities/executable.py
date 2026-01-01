from components.components import SystemEntity
from entities.entity import Entity


class Executable(Entity):
    def __init__(self):
        super().__init__()
        self.add(SystemEntity())