

from Utils.Camera import Camera
from Utils.EnemyFactory import EnemyFactory
from Utils.spatialGrid import SpatialGrid
from entities.Spawn_Patterns.EnemyPatterns import Grid_Enemies, Line_Enemies
from entities.UI.button import Button
from entities.playerPart import PlayerPart
from entities.projectile_related.projectile import ProjectilePool
from entities.system_Entities.Spawner import SpawnerEntity
from entities.system_Entities.camera import CameraEntity
from entities.base import Base
from registries.AnimationStateList import AnimationMode
from scenes.scene import Scene

from systems.CleanupSystem import CleanupSystem
from systems.Game_AutoAimingSystem import AutoAimingSystem
from systems.ProjectileSystem import ProjectileSystem
from systems.RotationSystem import RotationSystem
from systems.SpawnerSystem import SpawnerSystem
from systems.CameraSystem import CameraSystem
from systems.AnimationSystem import EventCleanerSystem, Events_AnimationSystem, Playback_AnimationSystem, State_AnimationSystem
from systems.Game_ParentFollowSystem import ParentFollowSystem
from systems.Game_enemy_AiSystem import Enemy_AI_MovementSystem, Enemy_AI_ShootingSystem
from systems.UI.UI_Pointer_inputSystem import UI_Pointer_InputSystem
from systems.UI.UI_button_inputSystem import UI_Button_InputSystem
from systems.UI.button_displaySystem import ButtonDisplaySystem
from systems.camera_zoomSystem import CameraZoomSystem
from systems.healthBar_displaySystem import HealthBar_DisplaySystem
from systems.world_renderSystem import WorldRenderSystem
from systems.Game_inputSystem import InputSystem
from systems.UI.commandSystem import CommandSystem
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
from systems.transform_cameraSystem import CameraTransformSystem


class PlayScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.shipConfig = {}
        self.boosterConfig = {}
        self.camera = Camera()
        self.spawner = EnemyFactory(self)
        self.collision_grid = SpatialGrid(50)
        self.proj_pool = ProjectilePool(500)

    def on_Create(self):
        self.systems = [
            InputSystem(self),
            CameraZoomSystem(self),
            UI_Pointer_InputSystem(self),
            UI_Button_InputSystem(self),

            CommandSystem(self),
            ShootingSystem(self),
            AutoAimingSystem(self),
            Events_AnimationSystem(self),
            State_AnimationSystem(self),

            Enemy_AI_ShootingSystem(self),
            Enemy_AI_MovementSystem(self),

            MovementSystem(self),

            ParentFollowSystem(self),
            CollisionSystem(self),
            DamageSystem(self),
            HealthSystem(self),
            Playback_AnimationSystem(self),

            LifetimeSystem(self),
            CleanupSystem(self),
            EventCleanerSystem(self),

            CameraSystem(self),

            SpawnerSystem(self),
            ButtonDisplaySystem(self),
            CameraTransformSystem(self),

            # DebugCollisionRenderSystem(enabled=True),/
            # HealthDraw(Projectiles=False, Entity=True, Orbit=False),
            OnScreenDebugSystem(self),

            HealthBar_DisplaySystem(self),
            ProjectileSystem(self),
            RotationSystem(self),
            WorldRenderSystem(self),  # Uses ViewPosition
        ]

        self.playerConfig = {
            "Pos": (400, 300),
            "Sprite": "player",
            "Anim": {
                "player-idle": Anim([], [(0, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
                # "player-move-left": Anim([], [(96,0,48,48), (48,0,48,48), (0,0,48,48)], 0, 0.1, AnimationMode.NORMAL),
                # "player-move-right": Anim([], [(96,0,48,48), (144,0,48,48), (192,0,48,48)], 0, 0.1, AnimationMode.NORMAL)
            },
            "col": (48, 48),
            "Vel": 420,
            "Cannon": True
        }

        self.boosterConfig = {
            "Pos": (100, 100),
            "Sprite": "booster",
            "Anim": {
                "booster-idle": Anim([], [(0, 0, 48, 48), (48, 0, 48, 48), (96, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
                "booster-move": Anim([], [(0, 48, 48, 48), (48, 48, 48, 48), (96, 48, 48, 48), (144, 48, 48, 48)], 0, 0.2, AnimationMode.LOOP)
            },
            "col": (48, 48),
        }

        self.cannonConfig = {
            "Pos": (100, 100),
            "Sprite": "player_cannon",
            "Anim": {
                "player_cannon-idle": Anim([], [(0, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
                "player_cannon-shoot": Anim([], [(0, 0, 48, 48), (48, 0, 48, 48), (96, 0, 48, 48), (144, 0, 48, 48), (192, 0, 48, 48), (240, 0, 48, 48), (288, 0, 48, 48)], 0, 0.07, AnimationMode.LOOP),
                "player_cannon-move": Anim([], [(0, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
            },
            "col": (48, 48),
        }

    def on_Enter(self):
        print("On Game")
        for system in self.systems:
            if type(system) in self.disabledSystems:
                system.Enabled = False

        cam = CameraEntity(self)
        pause = Button(self, "PAUSE")
        pause.get(Size).width = 50
        pause.get(Size).height = 50
        pause.get(Position).x = self.game.screen.display_surface.width / 2 - 25
        pause.get(Position).y = 10

        Headquarter = Base(self)
        Headquarter.get(Collider).width = 50
        Headquarter.get(Collider).height = 50

        Ship_Cannon = PlayerPart(self, config=self.cannonConfig)
        Ship_main = Player(self, config=self.playerConfig)
        Ship_Booster = PlayerPart(self, config=self.boosterConfig)

        Ship_Booster.get(Parent).entity = Ship_main
        Ship_Cannon.get(Parent).entity = Ship_main
        Ship_Cannon.add(Cannon(0.2))
        Ship_Cannon.add(AutoCannon(7))
        Ship_Cannon.add(ShootIntent())

        gridEnemy = SpawnerEntity(self, Grid_Enemies(
            (100, 100), (3, 3), Headquarter.get(Position), 32))

        self.camera.target = Ship_main

        self.entities.append(Ship_Cannon)
        self.entities.append(Ship_main)
        self.entities.append(Ship_Booster)
        self.entities.append(Headquarter)

        self.entities.append(gridEnemy)
        # self.entities.append(gridEnemy2)

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
