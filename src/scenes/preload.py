from references import SceneList
from scenes import mainMenu
from scenes.scene import Scene
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from baseGame import BaseGame

class Preload(Scene):
    def __init__(self, game: 'BaseGame') -> None:
        super().__init__(game)
        self.game = game

    def on_Create(self):
        self.game.asset_manager.load_assets()
    
    def on_Enter(self):
        print("On preload")
        self.game.scene_manager.replace(SceneList.MAIN_MENU)
    
    def on_Exit(self):
        return super().on_Exit()
    
    def on_Pause(self):
        return super().on_Pause()
    
    def on_Resume(self):
        return super().on_Resume()