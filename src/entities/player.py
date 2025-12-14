from components.components import Animation, Anim, Collider, Position, Sprite, Velocity
from components.intents import MovementIntent
from entities.entity import Entity
from spritesheet import Spritesheet

class Player(Entity):
    def __init__(self, game):
        super().__init__(game)

        self.add_component(Position(10, 10))
        self.add_component(Velocity(1200))
        self.add_component(Sprite())
        self.add_component(Animation(
            spritesheet="booster",
            animation = {
                "booster": Anim([], ((0,0,48,48), (48,0,48,48), (96,0,48,48)), 0, 0.2)
            }
        ))

        self.add_component(MovementIntent())
        # self.add_component(InputIntent())

        self.game = game
        self._build_Animation()

    def _build_Animation(self):
        animation = self.get_component("Animation")
        sprite = self.get_component("Sprite")

        spritesheet = Spritesheet(self.game.asset_manager.get_asset(animation.spritesheet), True)
        for key, anim in animation.anim.items():
            anim.frames = spritesheet.get_animation(anim.frame_coords, anim.frame_duration)
            anim.name = key
            animation.anim_list[anim.name] = anim.frames

            if animation.active_name == "":
                animation.active_anim = animation.anim_list[anim.name]
                animation.active_name = anim.name
                sprite.image = animation.active_anim.get_frame(0)