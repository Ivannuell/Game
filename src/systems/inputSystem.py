from inputManager import InputManager
from entities.entity import Entity
import pygame


class InputSystem:
    def __init__(self, inputManager: InputManager) -> None:
        self.inputManager = inputManager

    def update(self, entities: list[Entity], dt):
        movers = []
        shooters = []

        for entity in entities:
            if entity.has_component("MovementIntent") and entity.has_component("InputControlled"):
                movers.append(entity)

            if entity.has_component("FireIntent") and entity.has_component("Cannon"):
                shooters.append(entity)

        for shooter in shooters:
            fire = shooter.get_component("FireIntent")

            fire.fired = False

            if pygame.K_SPACE in self.inputManager.keys_down:
                fire.fired = True


        for mover in movers:
            movement_intent = mover.get_component("MovementIntent")

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
