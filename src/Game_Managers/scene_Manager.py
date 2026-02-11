from enum import Enum
from types import LambdaType
from typing import TYPE_CHECKING, Optional

from registries.SceneList import SceneList
from scenes.play import PlayScene
from scenes.mainMenu import MainMenu
from scenes.pause import Pause
from scenes.preload import Preload

if TYPE_CHECKING:
    from scenes.scene import Scene
    from baseGame import BaseGame

class SceneManager:
    def __init__(self, game: 'BaseGame'):
        self.game = game
        self._stack: list["Scene"] = []
        self._pending_op_stack: list[LambdaType] = []

        self._input_frozen = False
        self._update_frozen = False

        self.scene_registry: dict[SceneList, Scene] = {
            SceneList.PAUSE: Pause(game),
            SceneList.GAME: PlayScene(game),
            SceneList.MAIN_MENU: MainMenu(game),
            SceneList.PRELOAD: Preload(game)
        }

    @property
    def active_scene(self) -> Optional["Scene"]:
        if not self._stack:
            return None
        return self._stack[-1]
        

    def push(self, scene: SceneList):
        self._pending_op_stack.append(lambda: self._do_push(self.scene_registry.get(scene)))
        
    def pop(self):
        self._pending_op_stack.append(lambda: self._do_pop())

    def replace(self, scene: SceneList):
        self._pending_op_stack.append(lambda: self._do_replace(self.scene_registry.get(scene)))
        


    def _do_push(self, scene: "Scene | None"):
        if scene is None:
            raise Exception("Scene should be in the SceneList")

        if self._stack:
            self._stack[-1].on_Pause()

        scene.on_Create()
        scene.on_Enter()
        self._stack.append(scene)


    def _do_pop(self) -> None:
        if not self._stack:
            return

        top: 'Scene' = self._stack.pop()
        top.on_Exit()

        if self._stack:
            self._stack[-1].on_Resume()


    def _do_replace(self, scene: "Scene | None"):
        if scene is None:
            raise Exception("Scene should be in the SceneList")

        self._do_pop()
        self._do_push(scene)


    def _do_pending_operations(self):
        for operation in self._pending_op_stack:
            operation()
        self._pending_op_stack.clear()



    def handle_input(self, events):
        if self._input_frozen or not self._stack:
            return

        for scene in reversed(self._stack):
            scene.handle_input(events)
            scene.ui_manager.handle_event(events)
            scene.command_manager.flush()
            if scene.blocks_input:
                break
        

    def update(self, dt: float):
        self._do_pending_operations()

        if not self._stack:
            return

        for scene in reversed(self._stack):
            scene.update(dt)
            scene.ui_manager.update(dt)
            if scene.blocks_update:
                break

    def render(self, screen):
        for scene in self._stack:
            scene.render(screen)
            scene.ui_manager.draw(screen)