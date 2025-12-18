class CollisionCleanupSystem:
    def update(self, entities, dt):
        for e in entities:
            e.remove_component("CollidedWith")
