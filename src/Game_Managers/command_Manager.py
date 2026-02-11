from icecream import ic
from components.components import Command, CommandType
from entities.Utility_Entities.executable import Executable
        

class CommandManager:
    def __init__(self, scene):
        self.scene = scene
        self._queue = []

    def send(self, command):
        self._queue.append(command)

    def flush(self):
        for command in self._queue:
            if command == "PAUSE":
                pauseCommand = Executable(self.scene)
                pauseCommand.add(Command(CommandType.PAUSE))
                
                self.scene.entity_manager.add(pauseCommand)

            elif command == "RESUME":
                resumeCommand = Executable(self.scene)
                resumeCommand.add(Command(CommandType.RESUME))

                self.scene.entity_manager.add(resumeCommand)

        self._queue.clear()
