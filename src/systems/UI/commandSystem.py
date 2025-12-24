from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


import pygame
from components.components import Command, PointerState, CommandType
from entities.UI.executable import Executable
from systems.system import System



class CommandSystem(System):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Command):
                command = entity.get(Command)
                
                print(command.type)
                if command.type == CommandType.CHANGE_SCENE:
                    self.game.scene_manager.replace(command.payload)
                    entities.remove(entity)

                elif command.type == CommandType.EXIT:
                    print(entities)
                    pygame.quit()
                    exit()

                elif command.type == CommandType.PAUSE:
                    self.game.scene_manager.push("PAUSE")
                    entities.remove(entity)

                elif command.type == CommandType.RESUME:
                    self.game.screen.display_surface.fill("black")
                    self.game.scene_manager.pop()
                    entities.remove(entity)