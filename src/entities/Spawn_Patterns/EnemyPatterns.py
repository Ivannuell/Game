from abc import ABC, abstractmethod
import math

import pygame
from registries.EnemyList import EnemyList
from systems.SpawnerSystem import SpawnEvent

class SpawnPattern(ABC):
    @abstractmethod
    def reset(self): pass

    @abstractmethod
    def update(self, dt): pass

    @abstractmethod
    def is_done(self) -> bool: pass

    @abstractmethod
    def get_spawn_events(self) -> list:
        pass

class Line_SpawnPattern(SpawnPattern):
    def __init__(self, count, start, spacing, interval,game, target=None):
        self.count = count
        self.start = start
        self.spacing = spacing
        self.interval = interval
        self.timer = 0
        self.spawned = 0
        self.target = target
        self.game = game

    def reset(self):
        return super().reset()
    
    def update(self, dt):
        self.timer += dt
    
    def is_done(self) -> bool:
        return self.spawned >= self.count
    
    def get_spawn_events(self) -> list[SpawnEvent]:
        events = []
        while self.spawned <= self.count and self.timer >= self.interval:
            pos = pygame.Vector2(
                self.start.y + self.spawned * self.spacing,
                self.start.x
            )

            
            spawn = SpawnEvent()
            spawn.spawn = EnemyList.Normal
            spawn.position = pos

            if self.target:
                dx = self.target.x - self.start.x
                dy = self.start.y - self.target.y  # invert Y

                angle = math.atan2(dy, dx)
                spawn.direction = angle

            events.append(spawn)

            self.timer = 0
            self.spawned += 1
        
        return events
        