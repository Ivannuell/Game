from types import LambdaType
from typing import TYPE_CHECKING

from scenes.scene import Scene
if TYPE_CHECKING:
    from scenes.scene import Scene


class SceneManager:
    def __init__(self, game):
        self.game = game
        self._stack: list["Scene"] = []
        self._pending_op_stack: list[LambdaType] = []

        self._input_frozen = False
        self._update_frozen = False


    def push(self, scene):
        self._pending_op_stack.append(lambda: self._do_push(scene))
        
    def pop(self):
        self._pending_op_stack.append(lambda: self._do_pop())

    def replace(self, scene):
        self._pending_op_stack.append(lambda: self._do_replace(scene))
        


    def _do_push(self, scene: "Scene"):
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


    def _do_replace(self, scene: "Scene"):
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
            if scene.blocks_input:
                break

    def update(self, dt: float):
        self._do_pending_operations()

        if not self._stack:
            return

        for scene in reversed(self._stack):
            scene.update(dt)
            if scene.blocks_update:
                break

    def render(self, screen):
        for scene in self._stack:
            scene.render(screen)