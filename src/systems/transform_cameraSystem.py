import math

from entities.player import Player
from components.components import *
from entities.playerPart import PlayerPart
from systems.system import System


class CameraTransformSystem(System):
    def __init__(self, camera, screen_center):
        super().__init__()
        self.camera = camera
        self.cx, self.cy = screen_center

    def update(self, entities, dt):
        cos_r = math.cos(-self.camera.rotation)
        sin_r = math.sin(-self.camera.rotation)

        for e in entities:
            if not e.has(Position, ViewPosition):
                continue
            
            pos = e.get(Position)
            view = e.get(ViewPosition)

            # if type(e) is Player:
            #     view.x = 0
            #     view.y = 0
            #     continue

            # if type(e) is PlayerPart:
            #     view.x = 0
            #     view.y = 15
            #     continue

            # World → camera space
            dx = pos.x - self.camera.x
            dy = pos.y - self.camera.y

            cam_x = dx * cos_r - dy * sin_r
            cam_y = dx * sin_r + dy * cos_r

            # Camera → screen space
            view.x = cam_x
            view.y = cam_y
            # # Camera → screen space
            # view.x = self.cx + cam_x
            # view.y = self.cy + cam_y
