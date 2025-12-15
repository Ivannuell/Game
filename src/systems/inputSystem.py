from inputManager import InputManager
from entities.entity import Entity
import pygame

class InputSystem:
    def __init__(self, inputManager: InputManager) -> None:
        self.inputManager = inputManager

    def update(self, entities: list[Entity], dt):
        for entity in entities:
            try:
                movement_intent = entity.get_component("MovementIntent")
            except:
                continue

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
