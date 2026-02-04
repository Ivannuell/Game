from components.components import *
from entities.spaceship import Spaceship
from registries.AnimationStateList import AnimationMode
from registries.EnemyList import EnemyList
from registries.EntityConfigs import *


class SpaceshipFactory:
    def __init__(self, scene):
        self.scene = scene
        self.game = scene.game

    def create(self, enemy: EnemyList) -> Spaceship:   
        if enemy == EnemyList.Normal:
            e = Spaceship(self.scene, normal_EnemyConfig)
            angle = e.get(Rotation).angle
            e.add(Cannon(1))
            e.add(ManualAim(angle))
            e.add(Vision(10))
            e.add(Perception())
            e.add(Attacker())
            e.add(Target())
            
            e.add(Gold(10))

            return e

        elif enemy == EnemyList.Farmer:
            e = Spaceship(self.scene, normal_EnemyConfig)
            angle = e.get(Rotation).angle

            e.add(Cannon(0.5))
            e.add(ManualAim(angle))
            e.add(Vision(10))
            e.add(Perception())
            e.add(Farmer())
            e.add(Target())

            e.add(GoldContainer(1000))

            return e