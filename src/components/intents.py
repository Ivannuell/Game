
from components.components import Component

class MovementIntent(Component):
    def __init__(self):
        self.id = "MovementIntent"
        self.move_x = 0
        self.move_y = 0

# class InputIntent(Component):
#     def __init__(self):
#         self.id = "InputIntent"
#         self.key_down = False
#         self.key_up = False
#         self.mouse_click = (0, 0, 0)