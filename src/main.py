import pygame
import os
from screen import Screen
from game import BaseGame

class Launcher():
    def __init__(self):
        pygame.init()
        self.path = os.path.curdir

    def start(self):
        self.screen = Screen(1280, 720)
        self.game = BaseGame()

        self.game.set_screen(self.screen)
        self.game.start()

if __name__ == "__main__":
    launcher = Launcher()
    launcher.start()