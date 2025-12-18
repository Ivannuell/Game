

from entities.entity import Entity

class ProjectileBehaviourSystem:
    elapsed_time = 0

    def update(self, entities: list[Entity], dt):
        projectiles = []

        for entity in entities:
            if entity.has_component("Projectile"):
                projectiles.append(entity)

