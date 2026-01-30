from components.components import * 
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene
    from scenes.play import PlayScene


class CameraSystem(System):
    def __init__(self, scene: 'PlayScene'):
        super().__init__(scene)
        
    def update(self, entities: 'list[Scene]',  dt):
        if self.scene.camera.target is None:
            return

        target_pos = self.scene.camera.target.get(Position)
        target_rot = self.scene.camera.target.get(Rotation)

        self.scene.camera.x = target_pos.x
        self.scene.camera.y = target_pos.y

        # Follow rotation for forward orientation
        # self.camera.rotation = target_rot.rad_angle - SPRITE_FORWARD_OFFSET
