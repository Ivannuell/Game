
from scenes.scene import Scene

from systems.AnimationSystem import AnimationSystem
from systems.RenderSystem import RenderSystem
from systems.inputSystem import InputSystem
from systems.movementSystem import MovementSystem
from systems.collisionSystem import CollisionSystem
from systems.shootingSystem import ShootingSystem
from systems.collider_cleanerSystem import CollisionCleanupSystem
from systems.lifetimeSystem import LifetimeSystem
from systems.projectile_movementSystem import ProjectileMovementSystem
from systems.projectile_behaviourSystem import ProjectileBehaviourSystem
from systems.damageSystem import DamageSystem
from systems.healthSystem import HealthSystem

from systems.debugers.collideRectDebug import DebugCollisionRenderSystem
from systems.debugers.healthDraw_DebugerSystem import HealthDraw
from systems.debugers.onScreen_DebugerSystem import OnScreenDebugSystem

from components.components import *


from entities.player import Player
from entities.obstacle import Obstacle
from entities.enemy import Enemy


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

            CollisionCleanupSystem(),
            CollisionSystem(),
            
            DamageSystem(),
            HealthSystem(self.game),

            AnimationSystem(),

            DebugCollisionRenderSystem(self.game.screen),
            HealthDraw(self.game.screen),
            OnScreenDebugSystem(self.game),
            

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
        enemy = Enemy()

        self.entities.append(Ship)
        self.entities.append(Booster)
        self.entities.append(enemy)

        for entity in self.entities:
            entity.game = self.game
            entity.init_Entity()

    def on_Exit(self):
        self.entities.clear()