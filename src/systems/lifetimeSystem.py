from entities.entity import Entity

class LifetimeSystem:
    def __init__(self):
        pass


    def update(self, entities: list[Entity], dt):
        bullets: list[Entity] = []
        collided_bullets: list[Entity] = []

        for entity in entities:
            if entity.has_component("Projectile"):
                bullets.append(entity)

        for entity in entities:
            if entity.has_component("Projectile") and entity.has_component("CollidedWith"):
                collided_bullets.append(entity)

        for bullet in bullets:
            pos = bullet.get_component("Position")

            if pos.y <= 0:
                entities.remove(bullet)


        for bullet in collided_bullets:
            entities.remove(bullet)