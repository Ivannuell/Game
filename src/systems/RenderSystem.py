from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from screen import Screen

from systems.system import System

class RenderSystem(System):
    def render(self, entities: list["Entity"], screen: "Screen"):
        for entity in entities:
            try:
                sprite = entity.get_component('Sprite')
                position = entity.get_component('Position')
            except:
                continue

            screen.display_surface.blit(sprite.image, (position.x, position.y))

