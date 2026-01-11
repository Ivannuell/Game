from logging import config
from components.components import *
from components.intents import *
from entities.entity import Entity


class AnimationEvent(Entity):
    def __init__(self, config, game):
        super().__init__(game)
        self.add(Position(config["Posx"], config["Posy"]))
        self.add(ViewPosition())
        self.add(Animation(
            spritesheet=config["Spritesheet"],
            animation=config["Animation"],
        ))
        self.add(Sprite())
        self.add(AnimationState())
        self.add(AnimationPlayer())
        self.add(Size(32,32,1))

        self.init_Entity()
        