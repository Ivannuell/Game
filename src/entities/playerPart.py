from entities.entity import Entity

from components.components import *


class PlayerPart(Entity):
    def __init__(self, config):
        super().__init__()