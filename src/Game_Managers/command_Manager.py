from icecream import ic
from components.components import Command, CommandType
from entities.Utility_Entities.executable import Executable
        
class CMD:
    def __init__(self, command, payload):
        self.command = command
        self.payload = payload

        
class CommandManager:
    def __init__(self, scene):
        self.scene = scene
        self._queue: Command = []

    def send(self, command, payload=None):
        self._queue.append(CMD(command, payload))

    def flush(self):
        for command in self._queue:
            cmd = Executable(self.scene)

            if command.command == "PAUSE":
                cmd.add(Command(CommandType.PAUSE))
            
            elif command.command == "OPEN":
                if command.payload == 'shop':
                    cmd.add(Command(CommandType.OPEN_SHOP))
            
            elif command.command == "EXIT":
                cmd.add(Command(CommandType.EXIT))

            elif command.command == "RESUME":
                cmd.add(Command(CommandType.RESUME))

            elif command.command == "SPAWN":
                cmd.add(Command(CommandType.SPAWN_NORMAL, command.payload))

            elif command.command == "GOLD_DELIVERED":
                cmd.add(Command(CommandType.EARN_GOLD, command.payload))
            
            else:
                print(f"{self.__class__.__name__} -- Command {command.command} could not be determined")
                continue

            self.scene.entity_manager.add(cmd)

        self._queue.clear()
