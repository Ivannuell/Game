from systems.system import System

class CollisionCleanupSystem(System):
    def update(self, entities, dt):
        for e in entities:
            if e.has_component("CollidedWith"):
                e.remove_component("CollidedWith")
