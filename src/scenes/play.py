
from entities.UI.button import Button
from entities.playerPart import PlayerPart
from entities.system_Entities.camera import CameraEntity
from entities.obstacle import Obstacle
from helper import SPRITE_FORWARD_OFFSET, get_Angle
from scenes.scene import Scene

from systems.CameraSystem import CameraSystem
from systems.AnimationSystem import Playback_AnimationSystem, State_AnimationSystem
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
            CameraZoomSystem(self.game.input_manager),
            UI_Pointer_InputSystem(self.game),
            UI_Button_InputSystem(self.game),

            CommandSystem(self.game),
            ShootingSystem(self.game),
            Enemy_AI_ShootingSystem(),
            State_AnimationSystem(),


            Enemy_AI_MovementSystem(),
            MovementSystem(),
            ParentFollowSystem(),

            # OrbitSystem(),
            ProjectileBehaviourSystem(),
            ProjectileMovementSystem(),

            LifetimeSystem(),

            CollisionCleanupSystem(),
            CollisionSystem(),
            
            DamageSystem(),
            HealthSystem(),

            Playback_AnimationSystem(),

            CameraSystem(self.game.camera),

            ButtonDisplaySystem(),
            CameraTransformSystem(self.game.camera, (self.game.screen.display_surface.width /2, self.game.screen.display_surface.height /2 + 500)),

            # DebugCollisionRenderSystem(enabled=True),
            # HealthDraw(Projectiles=True, Entity=True, Orbit=False),
            OnScreenDebugSystem(self.game),
            
            WorldRenderSystem(self.game)
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
                "booster-idle": Anim([], [(0,0,48,48), (48,0,48,48), (96,0,48,48)], 0, 0.2),
                "booster-move": Anim([], [(0,48,48,48), (48,48,48,48), (96,48,48,48), (144,48,48,48)], 0, 0.2)
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

        cam = CameraEntity()
        pause = Button("PAUSE")
        pause.get(Size).width = 50
        pause.get(Size).height = 50
        pause.get(Position).x = self.game.screen.display_surface.width /2 - 25
        pause.get(Position).y = 10
                


        Base = Obstacle()

        Ship_main = Player(self.shipConfig)
        Ship_Booster = PlayerPart(self.boosterConfig)
        Ship_Booster.get(Parent).entity = Ship_main

        enemy = Enemy()
        enemy.get(Position).x = 400
        enemy.get(Position).y = 100
        enemy.get(Size).width = 60
        enemy.get(Size).height = 60
        enemy.get(Rotation).rad_angle = get_Angle(enemy, Base) - SPRITE_FORWARD_OFFSET

        enemy2 = Enemy()
        enemy2.get(Position).x = 200
        enemy2.get(Position).y = 100
        enemy2.get(Size).width = 60
        enemy2.get(Size).height = 60
        enemy2.get(Rotation).rad_angle = get_Angle(enemy2, Base) - SPRITE_FORWARD_OFFSET


        self.game.camera.target = Ship_main

        self.entities.append(Ship_main)
        self.entities.append(Ship_Booster)
        self.entities.append(Base)
        self.entities.append(enemy)
        self.entities.append(enemy2)

        self.entities.append(cam)
        self.entities.append(pause)

        for entity in self.entities:
            entity.game = self.game
            if entity.has(SystemEntity):
                continue

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