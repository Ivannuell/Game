
import random
from typing import TYPE_CHECKING
from warnings import deprecated
import pygame

from entities.Utility_Entities.Spawner import SpawnEvent
from entities.asteriods import Asteriod
from registries.EntityConfigs import *

if TYPE_CHECKING:
    from entities.entity import Entity
    from scenes.play import PlayScene

from components.components import *

from systems.system import System


class Spaceship_SpawningSystem(System):

    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:

            if not entity.has(Spawner):
                continue

            spawner = entity.get(EntitySpawner)
            faction = entity.get(FactionIdentity).faction

            pattern = spawner.pattern

            pattern.update_step(dt)

            for event in pattern.get_spawn_events():
                event.faction = faction
                self.scene.entity_manager.add(self.spawnSpaceship(event))

            if pattern.is_done():
                entity.add(Destroy())

    def spawnSpaceship(self, event: SpawnEvent):
        spaceship = self.scene.spaceshipFactory.create(event.spawn)

        spaceship.get(Position).set(event.position)
        spaceship.get(Rotation).angle = event.direction
        spaceship.get(FactionIdentity).faction = event.faction
        spaceship.get(CollisionIdentity).role = event.faction

        return spaceship

class Farm_SpawningSystem(System):
    def update(self, entities, dt):
        for z in entities:
            if not z.has(ZoneComponent):
                continue

            zone = z.get(ZoneComponent)
            current = self.count_farms_in_zone(entities, zone.id)

            if current >= zone.maxCount:
                continue

            zone.timer += dt
            if zone.timer < zone.spawn_delay:
                continue

            zone.timer = 0
            farm = Asteriod(self.scene, Asteriod1)
            farm.add(ZoneId(zone.id))

            farm.get(Position).set(
                pygame.Vector2(*self.spawn_at(zone.pos[0], zone.size[0]))
            )

            self.scene.entity_manager.add(farm)


    def count_farms_in_zone(self, entities, zone_id):
        return sum(
            1 for e in entities
            if e.has(Farm, ZoneId) and e.get(ZoneId).id == zone_id
        )
    
    def spawn_at(self, x, w):
        rand_x = random.randint(x - x//2, x + w)
        rand_y = random.randint(-4500, 4500)

        return rand_x, rand_y














class _Asteriods_SpawningSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities, dt):
        new_asteroids = []

        for e in entities:
            if not e.has(ZoneComponent):
                continue

            zone = e.get(ZoneComponent)
            zone.timer += dt

            if zone.count >= zone.maxCount:
                continue

            if zone.timer < zone.spawn_delay:
                continue

            zone.timer = 0.0  # reset timer

            ast = Asteriod(self.scene, Asteriod1)
            ast.add(ZoneId(zone.id))
            ast.get(Position).set(
                pygame.Vector2(*self.spawn_at(zone.pos[0], zone.size[0]))
            )

            new_asteroids.append(ast)
            zone.count += 1

        entities.extend(new_asteroids)


    def spawn_at(self, x, w):
        rand_x = random.randint(x, x + w)
        rand_y = random.randint(-5000, 5000)

        return rand_x, rand_y

    def create_rect(self, pos, size):
        return pygame.Rect(pos, size)

    @deprecated("Now does not use math to spawn randomly")
    def random_point_biased_to_vertical_center(self, width, height, sigma_ratio=0.5):
        # Y is uniform
        y = random.uniform(0, height)

        # X is biased toward center
        center_x = width / 2
        sigma = width * sigma_ratio

        while True:
            x = random.gauss(center_x, sigma)
            if 0 <= x <= width:
                break

        return x, y
