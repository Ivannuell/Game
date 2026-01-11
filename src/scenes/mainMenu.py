from typing import TYPE_CHECKING
from scenes.scene import Scene

from components.components import Position, Size

from entities.UI.button import Button

from systems.UI.UI_Pointer_inputSystem import UI_Pointer_InputSystem
from systems.UI.UI_button_inputSystem import UI_Button_InputSystem
from systems.UI.button_displaySystem import ButtonDisplaySystem
from systems.UI.commandSystem import CommandSystem

class MainMenu(Scene):
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

        for system in self.systems:
            if type(system) in self.disabledSystems:
                system.Enabled = False

        
        button1 = Button('PLAY', self.game)
        button1.get(Position).x = self.game.screen.display_surface.get_width() / 2 - button1.get(Size).width / 2
        button1.get(Position).y = 100

        button2 = Button('EXIT', self.game)
        button2.get(Position).x = self.game.screen.display_surface.get_width() / 2 - button2.get(Size).width / 2
        button2.get(Position).y = 250


        self.entities.append(button1)
        self.entities.append(button2)

    
    def on_Exit(self):
        return super().on_Exit()
    
    def on_Pause(self):
        return super().on_Pause()
    
    def on_Resume(self):
        return super().on_Resume()