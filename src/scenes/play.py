

from components.components import *
from entities.base import Base
from entities.player import Player
from entities.playerPart import PlayerPart
from entities.projectile_related.projectile import ProjectilePool
from entities.Spawn_Patterns.EnemyPatterns import Line_Enemies
from entities.UI.button import Button
from entities.Utility_Entities.camera import CameraEntity
from entities.Utility_Entities.Spawner import SpawnerEntity
from entities.Utility_Entities.zone import Zone
from registries.EntityConfigs import *
from scenes.scene import Scene
from systems.AnimationSystem import (EventCleanerSystem,
                                     Events_AnimationSystem,
                                     Playback_AnimationSystem,
                                     State_AnimationSystem)
from systems.camera_zoomSystem import CameraZoomSystem
from systems.CameraSystem import CameraSystem
from systems.CleanupSystem import CleanupSystem
from systems.collider_cleanerSystem import CollisionCleanupSystem
from systems.collisionSystem import CollisionSystem
from systems.damageSystem import DamageSystem
from systems.debugers.collideRectDebug import DebugCollisionRenderSystem
from systems.debugers.healthDraw_DebugerSystem import HealthDraw
from systems.debugers.onScreen_DebugerSystem import OnScreenDebugSystem
from systems.Game_AsteriodSystem import Asteriods_ManagementSystem
from systems.Game_AutoAimingSystem import AutoAimingSystem, AutoFireSystem
from systems.Game_enemy_AiSystem import (AI_AttackerDecisionSystem,
                                         AI_AttackerPerceptionSystem,
                                         AI_FarmerDecisionSystem,
                                         Enemy_AI_MovementSystem,
                                         Enemy_AI_ShootingSystem,
                                         Enemy_AI_TargetSystem)
from systems.Game_goldSystem import Earn_GoldSystem
from systems.Game_inputSystem import InputSystem
from systems.Game_ParentFollowSystem import ParentFollowSystem
from systems.Game_SpawnerSystem import (Enemy_SpawningSystem, Farm_SpawningSystem)
from systems.GridSystem import Grid_IndexSystem
from systems.headsUpDisplaySystem import HeadsUpDisplaySystem
from systems.healthBar_displaySystem import HealthBar_DisplaySystem
from systems.healthSystem import HealthSystem
from systems.lifetimeSystem import LifetimeSystem
from systems.movementSystem import MovementSystem
from systems.projectile_behaviourSystem import ProjectileBehaviourSystem
from systems.projectile_movementSystem import ProjectileMovementSystem
from systems.ProjectileSystem import ProjectileSystem
from systems.RotationSystem import RotationSystem
from systems.shootingSystem import ShootingSystem
from systems.transform_cameraSystem import CameraTransformSystem
from systems.UI.button_displaySystem import ButtonDisplaySystem
from systems.UI.commandSystem import CommandSystem
from systems.UI.UI_button_inputSystem import UI_Button_InputSystem
from systems.UI.UI_Pointer_inputSystem import UI_Pointer_InputSystem
from systems.world_renderSystem import WorldRenderSystem
from Utils.spatialGrid import SpatialGrid
from Utils.Camera import Camera
from Utils.EnemyFactory import EnemyFactory


class PlayScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

        self.camera: Camera = Camera()
        self.enemyFactory = EnemyFactory(self)
        self.proj_pool = ProjectilePool(500)

        self._grid = SpatialGrid(64)
        # self.player_grid = SpatialGrid(50)
        # self.enemy_grid = SpatialGrid(50)
        # self.asteriod_grid =SpatialGrid(64)

        self.player_Entity: Player = None

    def on_Create(self):
        self.systems = [
            InputSystem(self),
            CameraZoomSystem(self),
            UI_Pointer_InputSystem(self),
            UI_Button_InputSystem(self),

            CommandSystem(self),
            ShootingSystem(self),
            AutoAimingSystem(self),
            AutoFireSystem(self),
            Events_AnimationSystem(self),
            State_AnimationSystem(self),

            Farm_SpawningSystem(self),
            Enemy_SpawningSystem(self),

            CollisionSystem(self),

            AI_FarmerDecisionSystem(self),

            Enemy_AI_MovementSystem(self),
            Enemy_AI_ShootingSystem(self),
            Enemy_AI_TargetSystem(self),

            MovementSystem(self),

            ParentFollowSystem(self),
            DamageSystem(self),
            HealthSystem(self),
            Earn_GoldSystem(self),
            Playback_AnimationSystem(self),

            Asteriods_ManagementSystem(self),

            LifetimeSystem(self),
            EventCleanerSystem(self),

            CameraSystem(self),

            CameraTransformSystem(self),
            RotationSystem(self),


            Grid_IndexSystem(self),

            CleanupSystem(self),

            ButtonDisplaySystem(self),
            HealthBar_DisplaySystem(self),
            HeadsUpDisplaySystem(self),

            ProjectileSystem(self),
            WorldRenderSystem(self),

            OnScreenDebugSystem(self),
        ]

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

        EnemyBase = Base(self, EnemyBaseConfig)
        Headquarter = Base(self, PlayerBaseConfig)

        EnemyBase.get(Rotation).angle = math.radians(175)
        # EnemyBase.add(EnemyIntent())

        Headquarter.get(Collider).width = 50
        Headquarter.get(Collider).height = 50

        Ship_Cannon = PlayerPart(self, config=cannonConfig)
        Ship_main = Player(self, config=playerConfig)
        Ship_Booster = PlayerPart(self, config=boosterConfig)
        Ship_Booster.get(Parent).entity = Ship_main
        Ship_Cannon.get(Parent).entity = Ship_main
        Ship_Cannon.add(Cannon(0.5))
        Ship_Cannon.add(AutoAim(7))
        Ship_Cannon.add(ShootIntent())
        Ship_Cannon.add(Perception())

        zone1 = Zone(self, 1, 70, (1000, 0), (300, 10000))
        # zone2 = Zone(self, 2, 10, (-100, 0), (800, 10000))
        zone3 = Zone(self, 3, 30, (590, 0), (610, 10000))
        zone4 = Zone(self, 4, 30, (1440, 0), (610, 10000))
        # zone5 = Zone(self, 5, 10, (2100, 0), (800, 10000))

        asteriodSpawner = SpawnerEntity(self)
        asteriodSpawner.add(AsteriodSpawner())

        enemySpawner = SpawnerEntity(self)
        enemySpawner.add(EnemySpawner(Line_Enemies(
            3, EnemyBase.get(Position), 40, 1
        )))

        # ast = Asteriod(self, Asteriod1)
        # ast.get(Position).set(pygame.Vector2(0,0))wwwww

        self.camera.target = Ship_main
        self.player_Entity = Ship_main

        self.entities.append(Ship_Cannon)
        self.entities.append(Ship_main)
        self.entities.append(Ship_Booster)
        self.entities.append(Headquarter)
        self.entities.append(EnemyBase)

        # self.entities.append(ast)
        self.entities.append(zone1)
        # self.entities.append(zone2)
        self.entities.append(zone3)
        self.entities.append(zone4)
        # self.entities.append(zone5)

        self.entities.append(asteriodSpawner)
        self.entities.append(enemySpawner)

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
            Grid_IndexSystem,

            AI_AttackerPerceptionSystem,
            AI_AttackerDecisionSystem,

            Enemy_AI_MovementSystem,
            Enemy_AI_ShootingSystem,
            Enemy_AI_TargetSystem,
        ]

    def on_Resume(self):
        self.disabledSystems = []

    def on_Exit(self):
        self.disabledSystems = []
        self.entities.clear()
