

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene

import pygame
from components.components import PointerState, Position, Size
from systems.system import System


class UI_Pointer_InputSystem(System):
    def __init__(self, scene: 'Scene'):
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt: float):
        mouse_pos = self.input_manager.mouse_pos
        mouse_down = self.input_manager.mouse_buttons[0]

        for entity in entities:
            if not entity.has(PointerState):
                continue

            state: PointerState = entity.get(PointerState)
            pos = entity.get(Position)
            size = entity.get(Size)

            rect = pygame.Rect(pos.x, pos.y, size.width, size.height)

            # reset one-frame flags
            state.reset_frame()

            # -------- Hover logic --------
            is_hovering_now = rect.collidepoint(mouse_pos)

            if is_hovering_now and not state.hovering:
                state.entered = True

            if not is_hovering_now and state.hovering:
                state.exited = True

            state.hovering = is_hovering_now

            # -------- Click logic --------
            # Press begins on this entity
            if mouse_down and state.hovering and not state.pressed:
                state.clicked = True
                state.pressed = True

            # Release only if this entity owned the press
            if not mouse_down and state.pressed:
                state.released = True
                state.pressed = False

            # Optional: cancel press if pointer leaves
            if state.pressed and not state.hovering:
                state.pressed = False


