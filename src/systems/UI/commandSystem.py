import pygame
from components.components import Command, PointerState, CommandType
from entities.UI.executable import Executable
from entities.entity import Entity


class CommandSystem:
    def __init__(self, game) -> None:
        self.game = game

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Command):

                command = entity.get(Command)
                
                print(command.type)
                if command.type == CommandType.CHANGE_SCENE:
                    self.game.scene_manager.replace(command.payload)
                    entity.remove(entity)

                if command.type == CommandType.EXIT:
                    print(entities)
                    pygame.quit()
                    exit()
