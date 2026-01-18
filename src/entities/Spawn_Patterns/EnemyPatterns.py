from abc import ABC, abstractmethod
import math

import pygame
from Utils.helper import SPRITE_FORWARD_OFFSET
from registries.EnemyList import EnemyList
from systems.SpawnerSystem import SpawnEvent

class SpawnPattern(ABC):
    @abstractmethod
    def reset(self): pass

    @abstractmethod
    def update_step(self, dt): pass

    @abstractmethod
    def is_done(self) -> bool: pass

    @abstractmethod
    def get_spawn_events(self) -> list:
        pass

class Line_Enemies(SpawnPattern):
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
    
    def update_step(self, dt):
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


class Grid_Enemies(SpawnPattern):
    def __init__(self, startPos:tuple[int, int], gridSize: tuple[int, int], angle, spacing):
        self.timer = 0
        self.spawned = 0
        self.gridx, self.gridy = gridSize
        self.startPos = startPos
        self.target = angle
        self.spacing = spacing

    def is_done(self) -> bool:
        return self.spawned >= self.gridx * self.gridy
    
    def reset(self):
        return super().reset()
    
    def update_step(self, dt):
        self.timer += dt

    def get_spawn_events(self) -> list:
        events = []

        for x in range(self.gridx):
            for y in range(self.gridy):
                enemy = SpawnEvent()
                enemy.spawn = EnemyList.Normal
                enemy.position = pygame.Vector2(
                    self.startPos[0] + x * self.spacing, 
                    self.startPos[1] + y * self.spacing
                    )

                dx = self.target.x - self.startPos[0]
                dy = self.target.y - self.startPos[1]

                enemy.direction = math.atan2(dy, dx)

               
                # enemy.direction = math.radians(enemy.position.angle_to(pygame.Vector2(self.target.x, self.target.y)) + 46)
                # enemy.direction = 2
                self.spawned += 1
                events.append(enemy)

        return events



