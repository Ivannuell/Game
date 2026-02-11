



from components.components import Component, ComponentRegistry
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
    


@ComponentRegistry.register
class Window(Component):
    def __init__(self) -> None:
        super().__init__()
        self.displaying = False

    def toggle(self):
        self.displaying = not self.displaying
        

@ComponentRegistry.register
class Buttons(Component):
    def __init__(self) -> None:
        super().__init__()
        self.buttons = []