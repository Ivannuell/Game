

import pygame
from UI.Menus.menu import Menu
from UI.Widgets.window import Window
from UI.Widgets.button import Button
from UI.displayLayouts import GridLayout
from UI.styles import SHOP_STYLE


class Pause_Menu(Menu):
    def __init__(self, ui_manager, command_manager, pos=(200, 200), size=(200, 400)):
        super().__init__(pos, size)

        self.widgets.append(
            Window(self)
        )

        self.widgets.append(
            Button(
                self,
                pos=(10, 10),
                size=(20, 20),
                style=SHOP_STYLE,
                on_click=lambda: command_manager.send("RESUME")),
        )

        for i in range(30):
            layout = GridLayout((10, 50), 6, 10)
            size = (20, 20)

            self.widgets.append(
                Button(
                    self,
                    pos=layout.position(i, size),
                    size=size,
                    style=SHOP_STYLE,
                    on_click=lambda: print(i+1)
                ))
