from typing import TYPE_CHECKING

from registries.SceneList import SceneList

if TYPE_CHECKING:
    from scenes.scene import Scene
    from entities.entity import Entity

from entities.system_Entities.executable import Executable

from components.components import *

from systems.system import System


class UI_Button_InputSystem(System):
    def __init__(self, scene: 'Scene') -> None:
        super().__init__(scene)
        
    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Clickable):
                pointerState = entity.get(PointerState)
                buttonID = entity.get(Clickable).buttonID

                if buttonID == "PLAY" and pointerState.released:
                    exe = Executable(self.scene)
                    exe.add(Command(CommandType.CHANGE_SCENE, SceneList.GAME))
                    entities.append(exe)

                if buttonID == "EXIT" and pointerState.released:
                    exe = Executable(self.scene)
                    exe.add(Command(CommandType.EXIT))
                    entities.append(exe)

                if buttonID == "RESUME" and pointerState.released:
                    exe = Executable(self.scene)
                    exe.add(Command(CommandType.RESUME))
                    entities.append(exe)

                if buttonID == "RESTART" and pointerState.released:
                    exe = Executable(self.scene)
                    exe.add(Command(CommandType.RESTART, SceneList.GAME))
                    entities.append(exe)

                if buttonID == "PAUSE" and pointerState.released:
                    cmd = Executable(self.scene)
                    cmd.add(Command(CommandType.PAUSE, SceneList.PAUSE))
                    entities.append(cmd)


                      

                

                