import pygame

class InputManager:
    def __init__(self):
        self.keys_down = set()
        self.keys_pressed = set()
        self.keys_released = set()
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)
        self.wheel_delta = 0

    def begin_frame(self):
        self.keys_pressed.clear()
        self.keys_released.clear()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.keys_down.add(event.key)
            self.keys_pressed.add(event.key)

        elif event.type == pygame.KEYUP:
            self.keys_down.discard(event.key)
            self.keys_released.add(event.key)

        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_buttons = pygame.mouse.get_pressed()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_buttons = (False, False, False)

        elif event.type == pygame.MOUSEWHEEL:
            self.wheel_delta = event.y
