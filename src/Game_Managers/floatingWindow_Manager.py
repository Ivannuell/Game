class FloatingWindow_Manager:
    def __init__(self, scene):
        self.scene = scene
            
    def add(self, windowEntity):
        self.scene.entity_manager.add(windowEntity)