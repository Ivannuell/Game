

from components.components import Position, Size
from entities.entity import Entity


class Button(Entity):
    def __init__(self):
        super().__init__()

        self.add(Position(300, 300))
        self.add(Size(300, 100))
    