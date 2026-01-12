
import math
from EnemyFactory import EnemyFactory, EnemyList
from entities.Spawn_Patterns.EnemyPatterns import Line_SpawnPattern
from entities.UI.button import Button
from entities.playerPart import PlayerPart
from entities.system_Entities.Spawner import SpawnerEntity
from entities.system_Entities.camera import CameraEntity
from entities.obstacle import Obstacle
from registries.AnimationStateList import AnimationMode
from scenes.scene import Scene

import screen
from systems.CleanupSystem import CleanupSystem
from systems.ProjectileSystem import ProjectileSystem
from systems.RotationSystem import RotationSystem
from systems.SpawnerSystem import SpawnerSystem
from systems.CameraSystem import CameraSystem
from systems.AnimationSystem import EventCleanup_AnimationSystem, Events_AnimationSystem, Playback_AnimationSystem, State_AnimationSystem
from systems.Game_ParentFollowSystem import ParentFollowSystem
from systems.Game_enemy_AiSystem import Enemy_AI_MovementSystem, Enemy_AI_ShootingSystem
from systems.UI.UI_Pointer_inputSystem import UI_Pointer_InputSystem
from systems.UI.UI_button_inputSystem import UI_Button_InputSystem
from systems.UI.button_displaySystem import ButtonDisplaySystem
from systems.camera_zoomSystem import CameraZoomSystem
from systems.world_renderSystem import WorldRenderSystem
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
            RotationSystem(),
            CameraZoomSystem(self.game.input_manager),
            UI_Pointer_InputSystem(self.game),
            UI_Button_InputSystem(self.game),

            CommandSystem(self.game),
            ShootingSystem(self.game),
            Events_AnimationSystem(self.game),
            State_AnimationSystem(),

            Enemy_AI_ShootingSystem(),
            Enemy_AI_MovementSystem(),
            
            SpawnerSystem(self.game),
            MovementSystem(),

            ParentFollowSystem(),
            CollisionSystem(self.game),
            DamageSystem(),
            HealthSystem(),
            Playback_AnimationSystem(),

            LifetimeSystem(),
            CleanupSystem(),
            EventCleanup_AnimationSystem(self.game),


            CameraSystem(self.game.camera),

            ButtonDisplaySystem(),
            CameraTransformSystem(self.game.camera, (self.game.screen.display_surface.width /2, self.game.screen.display_surface.height /2 + 500)),

            # DebugCollisionRenderSystem(enabled=True),/
            # HealthDraw(Projectiles=False, Entity=True, Orbit=False),
            OnScreenDebugSystem(self.game),
            
            ProjectileSystem(self.game),
            WorldRenderSystem(self.game),
        ]

        self.playerConfig = {
            "Pos": (500, 100),
            "Sprite": "player",
            "Anim": {
                "player-idle": Anim([], [(96,0,48,48)], 0, 0.2, AnimationMode.LOOP),
                "player-move-left": Anim([], [(96,0,48,48), (48,0,48,48), (0,0,48,48)], 0, 0.1, AnimationMode.NORMAL),
                "player-move-right": Anim([], [(96,0,48,48), (144,0,48,48), (192,0,48,48)], 0, 0.1, AnimationMode.NORMAL)
            },
            "col": (48,48),
            "Vel": 420,
            "Cannon": True
        }

        self.boosterConfig = {
            "Pos": (100, 100),
            "Sprite": "booster",
            "Anim": {
                "booster-idle": Anim([], [(0,0,48,48), (48,0,48,48), (96,0,48,48)], 0, 0.2, AnimationMode.LOOP),
                "booster-move": Anim([], [(0,48,48,48), (48,48,48,48), (96,48,48,48), (144,48,48,48)], 0, 0.2, AnimationMode.LOOP)
            },
            "col": (48,48),
            "Vel": 420
        }
        

    def on_Enter(self):
        print("On Game")
        for system in self.systems:
            if type(system) in self.disabledSystems:
                system.Enabled = False

        cam = CameraEntity(self.game)
        pause = Button("PAUSE", self.game)
        pause.get(Size).width = 50
        pause.get(Size).height = 50
        pause.get(Position).x = self.game.screen.display_surface.width /2 - 25
        pause.get(Position).y = 10

        Base = Obstacle(self.game)
        Base.get(Collider).width = 50
        Base.get(Collider).height = 50

        Ship_main = Player(self.playerConfig, self.game)
        Ship_Booster = PlayerPart(self.boosterConfig, self.game)
        Ship_Booster.get(Parent).entity = Ship_main
        Ship_Booster.get(OffsetPosition).x = -15


                
        spawn_line = SpawnerEntity(Line_SpawnPattern(20, pygame.Vector2(200, 100), 50, 0.1, self.game, Base.get(ViewPosition)), self.game)
        spawn_line2 = SpawnerEntity(Line_SpawnPattern(20, pygame.Vector2(300, 100), 50, 0.1, self.game, Base.get(ViewPosition)), self.game)
        spawn_line3 = SpawnerEntity(Line_SpawnPattern(20, pygame.Vector2(400, 100), 50, 0.1, self.game, Base.get(ViewPosition)), self.game)
        spawn_line4 = SpawnerEntity(Line_SpawnPattern(20, pygame.Vector2(500, 100), 50, 0.1, self.game, Base.get(ViewPosition)), self.game)
        self.game.camera.target = Ship_main

        self.entities.append(Ship_main)
        self.entities.append(Ship_Booster)
        self.entities.append(Base)

        self.entities.append(spawn_line)
        self.entities.append(spawn_line2)
        self.entities.append(spawn_line3)
        self.entities.append(spawn_line4)

        self.entities.append(cam)
        self.entities.append(pause)

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