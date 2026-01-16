import math
from typing import TYPE_CHECKING

from entities.player import Player
from helper import ROT_SPEED

if TYPE_CHECKING:
    from entities.entity import Entity

from entities.system_Entities.executable import Executable
from scenes.scene_Manager import SceneList
from inputManager import InputManager
from systems.system import System
from components.components import *

import pygame


class InputSystem(System):
    def __init__(self, inputManager: InputManager, game) -> None:
        super().__init__()
        self.inputManager = inputManager
        self.game = game

    def update(self, entities: list["Entity"], dt):
        movers = []
        shooters = []

        for entity in entities:
            if entity.has(MovementIntent, InputControlled):
                movers.append(entity)


            if entity.has(FireIntent, Cannon, InputControlled):
                shooters.append(entity)

        # TESTING
        if pygame.K_ESCAPE in self.inputManager.keys_down:
            cmd = Executable(self.game)
            cmd.add(Command(CommandType.PAUSE, SceneList.PAUSE))
            entities.append(cmd)
            self.inputManager.keys_down.remove(pygame.K_ESCAPE)

        if pygame.K_F3 in self.inputManager.keys_pressed:
            self.game.profiler_overlay.toggle()
        # --------------

        for shooter in shooters:
            fire = shooter.get(FireIntent)

            if pygame.K_SPACE in self.inputManager.keys_down:
                fire.fired = True


        for mover in movers:
            movement_intent = mover.get(MovementIntent)
            rotation = mover.get(Rotation)

            movement_intent.reset()

            if pygame.K_a in self.inputManager.keys_down:
                rotation.angular_vel -= ROT_SPEED
                movement_intent.rotate_left = True
            if pygame.K_d in self.inputManager.keys_down:
                rotation.angular_vel += ROT_SPEED
                movement_intent.rotate_right = True


            if pygame.K_w in self.inputManager.keys_down:
                movement_intent.move_y -= 1
                movement_intent.move_x += 1


            # rotation.set_target(rotation.rad_angle)

            # rotation.rad_angle += ((rotation.target_angle) - (rotation.rad_angle)) * (dt * 9)

        