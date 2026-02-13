

import pygame
from UI.Menus.menu import Menu
from UI.Widgets.window import Window
from UI.Widgets.button import Button
from UI.displayLayouts import GridLayout
from UI.styles import SHOP_STYLE
from registries.EnemyList import EnemyList


class Pause_Menu(Menu):
    def __init__(self, ui_manager, command_manager, pos=(200, 200), size=(200, 400)):
        super().__init__(pos, size)

        width, height = size
        
        self.widgets.append(
            Window(self)
        )

        self.widgets.append(
            Button(
                self,
                pos=(width/2 - (width/3)/2, 20),
                size=(width/3, 20),
                style=SHOP_STYLE,
                text="RESUME",
                on_click=lambda: command_manager.send("RESUME")),
        )

        self.widgets.append(
            Button(
                self,
                pos=(width/2 - (width/3)/2, width/2 - (width/3)/2+20),
                size=(width/3, 20),
                style=SHOP_STYLE,
                text="EXIT",
                on_click=lambda: command_manager.send("EXIT")
            )
        )
