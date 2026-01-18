import math

from entities.player import Player
from Utils.helper import ROT_SPEED

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene

from entities.system_Entities.executable import Executable
from scenes.scene_Manager import SceneList
from systems.system import System
from components.components import *

import pygame


class InputSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)

    def update(self, entities: list["Entity"], dt):
        movers = []
        shooters = []

        for entity in entities:
            if entity.has(MovementIntent, InputControlled):
                movers.append(entity)


            if entity.has(ShootIntent, Cannon, InputControlled):
                shooters.append(entity)

        # TESTING
        if pygame.K_ESCAPE in self.input_manager.keys_down:
            cmd = Executable(self.scene)
            cmd.add(Command(CommandType.PAUSE, SceneList.PAUSE))
            entities.append(cmd)
            self.input_manager.keys_down.remove(pygame.K_ESCAPE)

        if pygame.K_F3 in self.input_manager.keys_pressed:
            self.profiler_overlay.toggle()
        # --------------

        for mover in movers:
            movement_intent = mover.get(MovementIntent)
            rotation = mover.get(Rotation)

            movement_intent.reset()

            if pygame.K_a in self.input_manager.keys_down:
                rotation.angular_vel -= ROT_SPEED
                movement_intent.rotate_left = True
            if pygame.K_d in self.input_manager.keys_down:
                rotation.angular_vel += ROT_SPEED
                movement_intent.rotate_right = True


            if pygame.K_w in self.input_manager.keys_down:
                movement_intent.move_y -= 1
                movement_intent.move_x += 1

        