
from entities.obstacle import Obstacle
from scenes.scene import Scene

from systems.CameraSystem import CameraSystem
from systems.AnimationSystem import AnimationSystem
from systems.Game_enemy_AiSystem import Enemy_AI_MovementSystem, Enemy_AI_ShootingSystem
from systems.RenderSystem import RenderSystem
from systems.Game_inputSystem import InputSystem
from systems.UI.commandSystem import CommandSystem
from systems.movementSystem import MovementSystem
from systems.collisionSystem import CollisionSystem
from systems.orbit_movementSystem import OrbitSystem
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
from entities.enemy import Enemy
from systems.transform_cameraSystem import CameraTransformSystem


class PlayScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.shipConfig = {}
        self.boosterConfig = {}

    def on_Create(self):
        self.systems = [
            InputSystem(self.game.input_manager, self.game),
            CommandSystem(self.game),
            ShootingSystem(self.game),
            MovementSystem(),
            OrbitSystem(),
            # Enemy_AI_MovementSystem(),
            # Enemy_AI_ShootingSystem(),
            ProjectileBehaviourSystem(),
            ProjectileMovementSystem(),

            LifetimeSystem(),

            CollisionCleanupSystem(),
            CollisionSystem(),
            
            DamageSystem(),
            HealthSystem(),

            AnimationSystem(),

            CameraSystem(self.game.camera),

            DebugCollisionRenderSystem(enabled=True),
            HealthDraw(Projectiles=True, Entity=True, Orbit=True),
            OnScreenDebugSystem(self.game),
            
            # RenderSystem(self.game.camera, (200, 500)),
            CameraTransformSystem(self.game.camera, (self.game.screen.display_surface.width /2, self.game.screen.display_surface.height /2)),
            # CameraTransformSystem(self.game.camera, (0,0)),
            RenderSystem(self.game)
        ]

        self.shipConfig = {
            "Pos": (100, 100),
            "Sprite": "ship",
            "Anim": {
                "ship-idle": Anim([], [(0,0,48,48)], 0, 0.2)
            },
            "col": (48,48),
            "Vel": 420,
            "Cannon": True
        }

        self.boosterConfig = {
            "Pos": (100, 100),
            "Sprite": "booster",
            "Anim": {
                "booster": Anim([], [(0,0,48,48), (48,0,48,48), (96,0,48,48)], 0, 0.2)
            },
            "col": (48,48),
            "Vel": 420
        }
        

    def on_Enter(self):
        print("On Game")
        print((self.game.screen.display_surface.width /2, self.game.screen.display_surface.height /2))
        for system in self.systems:
            if type(system) in self.disabledSystems:
                system.Enabled = False

                
        Ship = Player(self.shipConfig)

        obs = Obstacle()
        Ship.get(Orbit).center = obs
        self.game.camera.target = Ship

        self.entities.append(Ship)
        self.entities.append(obs)



        for entity in self.entities:
            entity.game = self.game
            entity.init_Entity()

    def on_Pause(self):
        self.disabledSystems = [
            InputSystem,
            ShootingSystem,
            MovementSystem,
            ProjectileBehaviourSystem,
            ProjectileMovementSystem,

            LifetimeSystem,

            CollisionCleanupSystem,
            CollisionSystem,
            
            DamageSystem,
            HealthSystem,

            DebugCollisionRenderSystem,
            HealthDraw,
            OnScreenDebugSystem,
        ]
    
    def on_Resume(self):
        self.disabledSystems = []

    def on_Exit(self):
        self.disabledSystems = []
        self.entities.clear()