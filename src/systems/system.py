# Refactor by using enums in System checkings
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.play import PlayScene
    from scenes.scene import Scene
    from Game_Managers.assetManager import AssetsManager
    from Game_Managers.inputManager import InputManager
    from Utils.systemProfiler import SystemProfiler
    from Utils.systemProfiler_overlay import DebugOverlaySystem
    from Game_Managers.scene_Manager import SceneManager


class System:
    def __init__(self, scene) -> None:
        self.Enabled = True
        self.scene: 'Scene | PlayScene' = scene
        self.asset_manager: 'AssetsManager' = scene.asset_manager
        self.input_manager: 'InputManager' = scene.input_manager
        self.profiler: 'SystemProfiler' = scene.profiler
        self.profiler_overlay: 'DebugOverlaySystem' = scene.profiler_overlay