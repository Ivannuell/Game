

from entities.entity import Entity

class ProjectileMovementSystem:


    def update(self, entities: list[Entity], dt):
        projectiles = []

        for entity in entities:

            if entity.has_component("Position") and entity.has_component("Projectile"):
                projectiles.append(entity)

        for projectile in projectiles:
            pos = projectile.get_component("Position")
            vel = projectile.get_component("Velocity")

            pos.y -= vel.speed 