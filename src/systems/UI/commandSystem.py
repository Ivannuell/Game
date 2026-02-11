from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

import pygame

from components.components import Command, CommandType

from entities.Utility_Entities.executable import Executable

from systems.system import System


class CommandSystem(System):
    def __init__(self, scene):
        super().__init__(scene)
        self.run_on_Pause = True

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Command):
                command = entity.get(Command)

                if command.type == CommandType.CHANGE_SCENE:
                    self.scene.game.scene_manager.replace(command.payload)
                    entities.remove(entity)

                elif command.type == CommandType.EXIT:
                    pygame.quit()
                    exit()

                elif command.type == CommandType.PAUSE:
                    self.scene.pause = True
                    self.scene.ui_manager.show('pause')
                    # self.scene.game.scene_manager.push(command.payload)
                    self.scene.entity_manager.remove(entity)


                elif command.type == CommandType.RESUME:
                    self.scene.pause = False
                    self.scene.ui_manager.hide('pause')
                    # self.scene.game.scene_manager.pop()
                    self.scene.entity_manager.remove(entity)

                elif command.type == CommandType.RESTART:
                    self.scene.game.scene_manager.pop()
                    self.scene.game.scene_manager.replace(command.payload)
                    entities.remove(entity)

