from logging import config
from components.components import *
from components.intents import *
from entities.entity import Entity


class AnimationEvent(Entity):
    def __init__(self, scene, config: dict = {}):
        super().__init__(scene)
        self.add(Position(config["Posx"], config["Posy"]))
        self.add(ViewPosition())
        self.add(Animation(
            spritesheet=config["Spritesheet"],
            animation=config["Animation"],
        ))
        self.add(Sprite())
        self.add(AnimationState())
        self.add(AnimationPlayer())
        self.add(Size(*config['size']))

        self.init_Entity()
        