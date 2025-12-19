from components.intents import MovementIntent
from entities.entity import Entity

from components.components import *
from components.intents import FireIntent

class Player(Entity):
    def __init__(self, config):
        super().__init__()

        self.__qualname__ = "Player"

        self.add_component(Animation(
            frame_scale=3,
            spritesheet=config["Sprite"],
            animation = config["Anim"]
        ))
        self.add_component(Position(config["Pos"][0], config["Pos"][1]))
        self.add_component(Velocity(config["Vel"]))
        self.add_component(Sprite())
        self.add_component(MovementIntent())
        self.add_component(Collider(48,48))
        self.add_component(InputControlled())
        self.add_component(FireIntent())
        self.add_component(Ship())
        self.add_component(CollisionIdentity(
            layer = [CollisionID.Players], 
            mask = [CollisionID.Enemies] 
        ))

        if "Cannon" in config:
            self.add_component(Cannon(0.5))
    
