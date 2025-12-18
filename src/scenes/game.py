
from scenes.scene import Scene

from systems.AnimationSystem import AnimationSystem
from systems.RenderSystem import RenderSystem
from systems.inputSystem import InputSystem
from systems.movementSystem import MovementSystem
from systems.collisionSystem import CollisionSystem
from systems.shootingSystem import ShootingSystem
from systems.collideRectDebug import DebugCollisionRenderSystem
from systems.lifetimeSystem import LifetimeSystem
from systems.projectile_movementSystem import ProjectileMovementSystem
from systems.projectile_behaviourSystem import ProjectileBehaviourSystem

from components.components import Animation, Anim, Collider, Position, Sprite, Velocity, Solid

from entities.player import Player


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def on_Enter(self):
        self.systems = [
            InputSystem(self.game.input_manager),
            ShootingSystem(self.game),
            MovementSystem(),
            ProjectileBehaviourSystem(),
            ProjectileMovementSystem(),
            LifetimeSystem(),
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
            "col": (48,48),
            "Vel": 420,
            "Cannon": True
        }

        boosterConfig = {
            "Pos": (100, 100),
            "Sprite": "booster",
            "Anim": {
                "booster": Anim([], ((0,0,48,48), (48,0,48,48), (96,0,48,48)), 0, 0.2)
            },
            "col": (48,48),
            "Vel": 420
        }

        Ship = Player(shipConfig)
        Booster = Player(boosterConfig)

        self.entities.append(Ship)
        self.entities.append(Booster)

        for entity in self.entities:
            entity.game = self.game
            entity.init_Entity()

    def on_Exit(self):
        self.entities.clear()