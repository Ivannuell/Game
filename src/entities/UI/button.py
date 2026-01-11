

from components.components import *
from entities.entity import Entity


class Button(Entity):
    def __init__(self, buttonID, game):
        super().__init__(game)
        self.add(Clickable(buttonID))
        self.add(Position(0, 300))
        self.add(Size(300, 100))
        self.add(PointerState())
        self.add(UiElement())