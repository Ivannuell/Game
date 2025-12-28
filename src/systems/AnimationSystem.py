from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

from systems.system import System
from components.components import *

class AnimationSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Sprite) and entity.has(Animation):
                sprite = entity.get(Sprite)
                animation = entity.get(Animation)

                sprite.image = animation.active_anim.get_frame(dt)
                sprite.original = animation.active_anim.get_frame(dt)