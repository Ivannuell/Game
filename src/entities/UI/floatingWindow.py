from components.UI_Components import *
from components.components import *
from entities.entity import Entity


class FloatingWindow(Entity):
    def __init__(self, scene):
        super().__init__(scene)
        self.add(Position(100, 100))
        self.add(Size(200, 200))
        self.add(Window())
        self.add(Buttons())