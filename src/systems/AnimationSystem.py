from spritesheet import Spritesheet
from assetManager import AssetsManager
from components.components import Sprite, Animation
from entities.entity import Entity

class AnimationSystem:
    def update(self, entities: list[Entity], dt):
        for entity in entities:
            sprite = entity.get_component("Sprite")
            animation = entity.get_component("Animation")

            if not sprite or not animation or not animation.active_anim:
                continue
     
            sprite.image = animation.active_anim.get_frame(dt)