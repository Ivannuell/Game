
from components.components import Component

class MovementIntent(Component):
    def __init__(self):
        self.id = "MovementIntent"
        self.move_x = 0
        self.move_y = 0
        
class FireIntent(Component):
    def __init__(self):
        self.id = "FireIntent"
        self.fired = False