from typing import NoReturn
from os import path

import pygame
from screen import Screen
from baseGame import BaseGame


class Launcher():
    def __init__(self):
        pygame.init()
        self.path: str = path.curdir

    def start(self)  -> NoReturn:
        self.screen = Screen(1280, 720)
        self.game = BaseGame()

        self.game.set_screen(self.screen)
        self.game.start()

if __name__ == "__main__": 
    launcher = Launcher()
    launcher.start()