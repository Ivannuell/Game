
import pygame
from scenes.scene import Scene

from entities.UI.button import Button

from components.components import Position, Size

from systems.UI.UI_Pointer_inputSystem import UI_Pointer_InputSystem
from systems.UI.UI_button_inputSystem import UI_Button_InputSystem
from systems.UI.button_displaySystem import ButtonDisplaySystem
from systems.UI.commandSystem import CommandSystem


class Pause(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def on_Create(self):
        self.systems = [
            UI_Pointer_InputSystem(self.game),
            UI_Button_InputSystem(self.game),
            CommandSystem(self.game),

            ButtonDisplaySystem()
        ]
    
    def on_Enter(self):
        resume = Button("RESUME")
        resume.get(Position).x = self.game.screen.display_surface.get_width() / 2 - resume.get(Size).width / 2
        resume.get(Position).y = 100

        exit = Button('EXIT')
        exit.get(Position).x = self.game.screen.display_surface.get_width() / 2 - exit.get(Size).width / 2
        exit.get(Position).y = 250

        restart = Button('RESTART')
        restart.get(Position).x = self.game.screen.display_surface.get_width() / 2 - restart.get(Size).width / 2
        restart.get(Position).y = 400

        self.entities.append(resume)
        self.entities.append(exit)
        self.entities.append(restart)


    def on_Exit(self):
        self.entities.clear()
    
    def on_Pause(self):
        return super().on_Pause()   
    
    def on_Resume(self):
        return super().on_Resume()