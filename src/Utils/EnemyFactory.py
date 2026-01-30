from components.components import *
from entities.enemy import Enemy
from registries.AnimationStateList import AnimationMode
from registries.EnemyList import EnemyList
from registries.EntityConfigs import *


class EnemyFactory:
    def __init__(self, scene):
        self.scene = scene
        self.game = scene.game

    def create(self, enemy: EnemyList) -> Enemy:   
        if enemy == EnemyList.Normal:
            e = Enemy(self.scene, normal_EnemyConfig)
            angle = e.get(Rotation).angle
            e.add(Cannon(1))
            e.add(ManualAim(angle))
            e.add(Vision(10))
            e.add(Perception())
            # e.add(Attacker())
            e.add(Farmer())
            
            e.add(Gold(10))

            return e

        elif enemy == EnemyList.Farmer:
            e = Enemy(self.scene, farmer_EnemyConfig)