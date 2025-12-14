
from scenes.scene import Scene
from systems.AnimationSystem import AnimationSystem
from systems.RenderSystem import RenderSystem
from systems.inputSystem import InputSystem
from systems.movementSystem import MovementSystem
from entities.player import Player


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def on_Enter(self):
        self.systems = [
            InputSystem(self.game.input_manager),
            MovementSystem(),
            AnimationSystem(),
            RenderSystem(self.game.screen)

        ]

        player = Player(self.game)

        self.entities.append(player)

    def on_Exit(self):
        self.entities.clear()