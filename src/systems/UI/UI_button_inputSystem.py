from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from baseGame import BaseGame
    from entities.entity import Entity


from entities.UI.executable import Executable
from scenes.game import GameScene
import pygame
from components.components import *
from systems.system import System


class UI_Button_InputSystem(System):
    def __init__(self, game: 'BaseGame') -> None:
        super().__init__()
        self.game = game
        
    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Clickable):
                pointerState = entity.get(PointerState)
                buttonID = entity.get(Clickable).buttonID

                if pointerState.clicked:
                    print("Clicked")

                if buttonID == "PLAY" and pointerState.released:
                    exe = Executable()
                    exe.add(Command(CommandType.CHANGE_SCENE, GameScene(self.game)))
                    entities.append(exe)

                if buttonID == "EXIT" and pointerState.released:
                    exe = Executable()
                    exe.add(Command(CommandType.EXIT))
                    entities.append(exe)

                if buttonID == "RESUME" and pointerState.released:
                    exe = Executable()
                    exe.add(Command(CommandType.RESUME))
                    entities.append(exe)

                      

                

                