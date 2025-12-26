from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from screen import Screen

from systems.system import System
from components.components import *

class RenderSystem(System):
    def __init__(self) -> None:
        super().__init__()
    def render(self, entities: list["Entity"], screen: "Screen"):
        for entity in entities:
            if not entity.has(Sprite, Position):
                continue
            
            sprite = entity.get(Sprite)
            position = entity.get(Position)

            screen.display_surface.blit(sprite.image, (position.x, position.y))

