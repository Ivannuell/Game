from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

import pygame

from components.components import Command, CommandType

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

                if command.type == CommandType.CHANGE_SCENE:
                    self.game.scene_manager.replace(command.payload)
                    entities.remove(entity)

                elif command.type == CommandType.EXIT:
                    pygame.quit()
                    exit()

                elif command.type == CommandType.PAUSE:
                    self.game.scene_manager.push(command.payload)
                    entities.remove(entity)

                elif command.type == CommandType.RESUME:
                    self.game.scene_manager.pop()
                    entities.remove(entity)
