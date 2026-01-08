from components.components import * 
from systems.system import System


class CameraSystem(System):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def update(self, entities,  dt):
        if self.camera.target is None:
            return

        target_pos = self.camera.target.get(Position)
        target_rot = self.camera.target.get(Rotation)

        # Follow position
        self.camera.x = target_pos.x
        self.camera.y = target_pos.y

        # Follow rotation for forward orientation
        self.camera.rotation = target_rot.rad_angle - SPRITE_FORWARD_OFFSET
