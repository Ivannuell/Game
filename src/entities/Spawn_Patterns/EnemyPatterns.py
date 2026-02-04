from abc import ABC, abstractmethod
import math

import pygame
from Utils.helper import SPRITE_FORWARD_OFFSET, point_towards
from components.components import Position
from registries.EnemyList import EnemyList
from systems.Game_SpawnerSystem import SpawnEvent

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

class Line_Entities(SpawnPattern):
    def __init__(self, count, start, spacing, interval, enemyType, target=None):
        self.count = count
        self.start = start
        self.spacing = spacing
        self.interval = interval
        self.timer = 0
        self.spawned = 0
        self.target = target
        self.enemyType = enemyType

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
                self.start.x + self.spawned * self.spacing,
                self.start.y
            )
     
            spawn = SpawnEvent()
            spawn.spawn = self.enemyType
            spawn.position = pos
            # spawn.direction = point_towards(pos)
            
            spawn.target = self.target
            spawn.direction = 2
            
            if self.target:
                pos = self.target.get(Position)
                spawn.direction = point_towards(self.start, pos)

            events.append(spawn)

            self.timer = 0
            self.spawned += 1
        
        return events


class Grid_Entities(SpawnPattern):
    def __init__(self, startPos:tuple[int, int], gridSize: tuple[int, int], target, spacing, EnemyType: EnemyList):
        self.timer = 0
        self.spawned = 0
        self.gridx, self.gridy = gridSize
        self.startPos = startPos
        self.target = target
        self.spacing = spacing
        self.EnemyType = EnemyType

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
                target_pos = self.target.get(Position)

                enemy = SpawnEvent()
                enemy.spawn = self.EnemyType
                enemy.position = pygame.Vector2(
                    self.startPos[0] + x * self.spacing, 
                    self.startPos[1] + y * self.spacing
                    )
                enemy.direction = point_towards(enemy.position, target_pos)
                enemy.target = self.target

                self.spawned += 1
                events.append(enemy)

        return events



