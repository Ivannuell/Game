import math
from components.components import *
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.play import PlayScene


class CameraTransformSystem(System):
    def __init__(self, scene: 'PlayScene'):
        super().__init__(scene)

    def update(self, entities, dt):
        cos_r = math.cos(-self.scene.camera.rotation)
        sin_r = math.sin(-self.scene.camera.rotation)

        for e in entities:
            if not e.has(Position, ViewPosition):
                continue
            
            pos = e.get(Position)
            view = e.get(ViewPosition)

            # World → camera space
            dx = pos.x - self.scene.camera.x
            dy = pos.y - self.scene.camera.y

            cam_x = dx * cos_r - dy * sin_r
            cam_y = dx * sin_r + dy * cos_r

            # Camera → screen space
            view.x = cam_x
            view.y = cam_y

