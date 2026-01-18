
from components.components import Zoom
from Utils.helper import clamp_value
from scenes.scene import Scene
from systems.system import System

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.scene import Scene


class CameraZoomSystem(System):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Zoom):
                zoom = entity.get(Zoom)

                # Mouse wheel input is discrete
                if self.input_manager.wheel_delta > 0:
                    zoom.target_zoom *= zoom.zoom_step
                elif self.input_manager.wheel_delta < 0:
                    zoom.target_zoom /= zoom.zoom_step

                # Clamp target zoom
                zoom.target_zoom = clamp_value(zoom.target_zoom, zoom.min_zoom, zoom.max_zoom)

                # Smooth zoom
                zoom.zoom += (zoom.target_zoom - zoom.zoom) * 9 * dt

                # Snap prevention
                if abs(zoom.zoom - zoom.target_zoom) < 1e-3:
                    zoom.zoom = zoom.target_zoom

            # Reset wheel delta after processing
        self.input_manager.wheel_delta = 0



