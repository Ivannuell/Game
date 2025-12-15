
# from scenes.scene import Scene
from scenes.scene import Scene

from systems.AnimationSystem import AnimationSystem
from systems.RenderSystem import RenderSystem
from systems.inputSystem import InputSystem
from systems.movementSystem import MovementSystem
from systems.collisionSystem import CollisionSystem
from systems.collideRectDebug import DebugCollisionRenderSystem

from components.components import Animation, Anim, Collider, Position, Sprite, Velocity, Solid

from entities.player import Player
from entities.obstacle import Obstacle


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def on_Enter(self):
        self.systems = [
            InputSystem(self.game.input_manager),
            MovementSystem(),
            CollisionSystem(),
            AnimationSystem(),
            DebugCollisionRenderSystem(self.game.screen),
            RenderSystem(self.game.screen)

        ]


        shipConfig = {
            "Pos": (100, 100),
            "Sprite": "ship",
            "Anim": {
                "ship-idle": Anim([], [(0,0,48,48)], 0, 0.2)
            },
            "col": (48,48)
        }

        boosterConfig = {
            "Pos": (100, 150),
            "Sprite": "booster",
            "Anim": {
                "booster": Anim([], ((0,0,48,48), (48,0,48,48), (96,0,48,48)), 0, 0.2)
            },
            "col": (48,48)
        }

        configs = {
            "Ship": shipConfig,
            "Booster": boosterConfig
        }

        Ship = Player(self.game, configs)

    def on_Exit(self):
        self.entities.clear()