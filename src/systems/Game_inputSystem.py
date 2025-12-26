from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity

from entities.UI.executable import Executable
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
            if entity.has(MovementIntent) and entity.has(InputControlled):
                movers.append(entity)

            if entity.has(FireIntent) and entity.has(Cannon):
                shooters.append(entity)

        # TESTING
        if pygame.K_ESCAPE in self.inputManager.keys_down:
            cmd = Executable()
            cmd.add(Command(CommandType.PAUSE, SceneList.PAUSE))
            entities.append(cmd)
            self.inputManager.keys_down.remove(pygame.K_ESCAPE)
        # --------------

        for shooter in shooters:
            fire = shooter.get(FireIntent)

            fire.fired = False

            if pygame.K_SPACE in self.inputManager.keys_down:
                fire.fired = True


        for mover in movers:
            movement_intent = mover.get(MovementIntent)

            movement_intent.move_y = 0
            movement_intent.move_x = 0

            if pygame.K_a in self.inputManager.keys_down:
                movement_intent.move_x -= 1
            if pygame.K_d in self.inputManager.keys_down:
                movement_intent.move_x += 1
            if pygame.K_s in self.inputManager.keys_down:
                movement_intent.move_y += 1
            if pygame.K_w in self.inputManager.keys_down:
                movement_intent.move_y -= 1


        