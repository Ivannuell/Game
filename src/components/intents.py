
from components.components import Component

class MovementIntent(Component):
    def __init__(self):
        super().__init__("MovementIntent")
        self.move_x = 0
        self.move_y = 0
        
class FireIntent(Component):
    def __init__(self):
        super().__init__( "FireIntent")
        self.fired = False