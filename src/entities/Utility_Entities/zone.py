from components.components import *
from entities.entity import Entity


class Zone(Entity):
    def __init__(self, idm, scene, maxcount, pos, size):
        super().__init__(scene)
        self.alive = True
        self.add(UtilityEntity())
        self.add(ZoneComponent(idm, maxcount, pos, size))