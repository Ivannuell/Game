from icecream import ic
from components.components import Command, CommandType
from entities.Utility_Entities.executable import Executable
        

class CommandManager:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self._queue = []

    def send(self, command):
        self._queue.append(command)

    def flush(self):
        scene = self.scene_manager.active_scene
        if not scene:
            return

        for command in self._queue:
            if command == "PAUSE":
                pauseCommand = Executable(scene)
                pauseCommand.add(Command(CommandType.PAUSE))
                
                scene.entity_manager.add(pauseCommand)

            elif command == "RESUME":
                resumeCommand = Executable(scene)
                resumeCommand.add(Command(CommandType.RESUME))

                scene.entity_manager.add(resumeCommand)

        self._queue.clear()
