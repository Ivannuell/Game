from inputManager import InputManager
from systems.system import System
from components.components import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity


import pygame


class InputSystem(System):
    def __init__(self, inputManager: InputManager) -> None:
        self.inputManager = inputManager

    def update(self, entities: list["Entity"], dt):
        movers = []
        shooters = []

        for entity in entities:
            if entity.has(MovementIntent) and entity.has(InputControlled):
                movers.append(entity)

            if entity.has(FireIntent) and entity.has(Cannon):
                shooters.append(entity)

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


        