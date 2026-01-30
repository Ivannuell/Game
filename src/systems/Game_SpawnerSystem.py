
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


class Enemy_SpawningSystem(System):

    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:

            if not entity.has(EnemySpawner):
                continue

            spawner = entity.get(EnemySpawner)
            pattern = spawner.pattern

            pattern.update_step(dt)

            for event in pattern.get_spawn_events():
                entities.append(self.spawnEnemy(event))

            if pattern.is_done():
                entity.add(Destroy())

    def spawnEnemy(self, event: SpawnEvent):
        enemy = self.scene.enemyFactory.create(event.spawn)

        enemy_pos = enemy.get(Position)
        enemy.add(Target(event.target))

        enemy_pos.set(event.position)
        enemy.get(Rotation).angle = event.direction

        return enemy


class Asteriods_SpawningSystem(System):
    def __init__(self, scene: 'PlayScene') -> None:
        super().__init__(scene)

    def update(self, entities: 'list[Entity]', dt):
        asteriods = []

        for e in entities:
            if not e.has(ZoneComponent):
                continue

            zone = e.get(ZoneComponent)

            if zone.count != zone.maxCount:
                ast = Asteriod(self.scene, Asteriod1)
                ast.add(ZoneId(zone.id))
                ast.get(Position).set(pygame.Vector2(*self.spawn_at(zone.pos[0], zone.size[0])))
                asteriods.append(ast)
                zone.count += 1

        entities.extend(asteriods)

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
