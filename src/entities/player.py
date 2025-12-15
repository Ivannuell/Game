from components.intents import MovementIntent
from entities.entity import Entity
from spritesheet import Spritesheet
from components.components import Animation, Anim, Collider, Position, Sprite, Velocity, Solid

class Player(Entity):
    def __init__(self, game, configs):
        super().__init__(game)

        self.add_component(Position(10, 10))
        self.add_component(Velocity(420))
        self.add_component(Sprite())
        self.add_component(Animation(
            frame_scale=3,
            spritesheet="booster",
            animation = {
                "booster": Anim([], ((0,0,48,48), (48,0,48,48), (96,0,48,48)), 0, 0.2)
            }
        ))

        self.add_component(MovementIntent())
        self.add_component(Collider(48,48))
        self.add_component(Solid())

        self.game = game
        self._init_Entity()

    def set_image(self, image):
        self.get_component("Sprite").image = self.game.asset_manager.get_asset(image)