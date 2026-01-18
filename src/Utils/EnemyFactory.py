from components.components import *
from entities.enemy import Enemy
from registries.AnimationStateList import AnimationMode
from registries.EnemyList import EnemyList


class EnemyFactory:
    def __init__(self, scene):
        self.scene = scene
        self.game = scene.game
        self.normal_EnemyConfig = {
            "Animation": {                
                "spritesheet": "enemy1",
                "animation": {
                    "enemy1-idle": Anim([], [(0,0,32,32)], 0, 0.2, AnimationMode.LOOP)
                },
            },
            "Position": (0,0),
            "Collider": (32,32),
            "Velocity": (10),
            "Cannon": (0.4),
            "Size": (32,32,1),
            "Health": (100)
        }

    def create(self, enemy: EnemyList) -> Enemy:   
        if enemy == EnemyList.Normal:
            e = Enemy(self.scene, self.normal_EnemyConfig)

            return e