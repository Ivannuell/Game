
from components.components import Component, ComponentRegistry


@ComponentRegistry.register
class Play_CollisionImpact_Event(Component):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.pos_x = x
        self.pos_y = y

@ComponentRegistry.register
class AnimationPlayer(Component):
    def __init__(self) -> None:
        super().__init__()

