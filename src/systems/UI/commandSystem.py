from typing import TYPE_CHECKING

from components.data_compnents import Item
from entities.Spawn_Patterns.EnemyPatterns import Line_Entities
from entities.Utility_Entities.Spawner import SpawnerEntity
from registries.EnemyList import EnemyList
if TYPE_CHECKING:
    from entities.entity import Entity

import pygame

from components.components import *

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

                elif command.type == CommandType.EXIT:
                    pygame.quit()
                    exit()

                elif command.type == CommandType.PAUSE:
                    self.scene.pause = True
                    self.scene.ui_manager.show('pause')

                elif command.type == CommandType.RESUME:
                    self.scene.pause = False
                    self.scene.ui_manager.hide('pause')

                elif command.type == CommandType.SPAWN_NORMAL:
                    if command.payload == "Farmer":
                        spawn = EnemyList.Farmer
                    elif command.payload == "Attacker":
                        spawn = EnemyList.Normal
                    else:
                        spawn = EnemyList.Farmer

                    self.scene.base_spawner.add(
                        EntitySpawner([
                            Line_Entities(0, Position(0, 100),
                                          0, 0.5, spawn, self.scene.enemy_base),
                        ])
                    )

                elif command.type == CommandType.EARN_GOLD:
                    gold, owner = command.payload
                    owner.get(GoldContainer).gold += gold

                elif command.type == CommandType.OPEN_SHOP:
                    self.scene.ui_manager.toggle('shop', payload=[
                            Item(name="Farmer", price=100),
                            Item(name="Attacker", price=150),
                          ])
                
                else:
                    print(f"Command {command.command} could not be determined")
                    continue

                self.scene.entity_manager.remove(entity)
