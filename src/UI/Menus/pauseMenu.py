

import pygame
from UI.Menus.menu import Menu
from UI.Widgets.window import Window
from UI.Widgets.button import Button
from UI.styles import SHOP_STYLE



class Pause_Menu(Menu):
    def __init__(self, ui_manager, command_manager, rect=(0,0, 300, 100)):
        super().__init__(rect)
        
        def resume():
            command_manager.send("RESUME")
            ui_manager.hide('pause')

        self.widgets.append(
            Window(self)
        )

        self.widgets.append(
            Button(
                self,
                pos= (10, 10),
                size= (20, 20),
                style= SHOP_STYLE,
                on_click= resume)
                )
        

        
        
