from systems.system import System
from entities.entity import Entity

class AnimationSystem(System):
    def update(self, entities: list[Entity], dt):
        for entity in entities:
            try:
                sprite = entity.get_component("Sprite")
                animation = entity.get_component("Animation")
            except Exception:
                if not entity.has_component("Sprite") or not entity.has_component("Animation"):
                    if not animation.active_anim:
                        continue

            sprite.image = animation.active_anim.get_frame(dt)