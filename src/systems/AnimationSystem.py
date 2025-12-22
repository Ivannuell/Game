from systems.system import System
from entities.entity import Entity
from components.components import *

class AnimationSystem(System):
    def update(self, entities: list[Entity], dt):
        for entity in entities:
            if entity.has(Sprite) and entity.has(Animation):
                sprite = entity.get(Sprite)
                animation = entity.get(Animation)

                sprite.image = animation.active_anim.get_frame(dt)