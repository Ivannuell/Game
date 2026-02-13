from components.components import Anim
from registries.AnimationStateList import AnimationMode


playerConfig = {
    "Pos": (100, 100),
    "Sprite": "player",
    "Anim": {
        "player-idle": Anim([], [(96,0,48,48)], 0, 0.2, AnimationMode.LOOP),
        "player-move-left": Anim([], [(96,0,48,48), (48,0,48,48), (0,0,48,48)], 0, 0.1, AnimationMode.NORMAL),
        "player-move-right": Anim([], [(96,0,48,48), (144,0,48,48), (192,0,48,48)], 0, 0.1, AnimationMode.NORMAL)
    },
    "col": (48, 48),
    "Vel": 400,
}

boosterConfig = {
    "Pos": (100, 100),
    "Sprite": "booster",
    "Anim": {
        "booster-idle": Anim([], [(0, 0, 48, 48), (48, 0, 48, 48), (96, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
        "booster-move": Anim([], [(0, 48, 48, 48), (48, 48, 48, 48), (96, 48, 48, 48), (144, 48, 48, 48)], 0, 0.2, AnimationMode.LOOP)
    },
    "col": (48, 48),
}

cannonConfig = {
    "Pos": (100, 100),
    "Sprite": "player_cannon",
    "Anim": {
        "player_cannon-idle": Anim([], [(0, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
        "player_cannon-shoot": Anim([], [(0, 0, 48, 48), (48, 0, 48, 48), (96, 0, 48, 48), (144, 0, 48, 48), (192, 0, 48, 48), (240, 0, 48, 48), (288, 0, 48, 48)], 0, 0.07, AnimationMode.LOOP),
        "player_cannon-move": Anim([], [(0, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP),
    },
    "col": (48, 48),
}

PlayerBaseConfig = {
    "Position": (0, 100),
    "Spritesheet": "ship",
    "Animation": {
        "ship-idle": Anim([], [(0, 0, 48, 48)], 0, 0.2, AnimationMode.LOOP)
    },
    "Size": (48, 48, 4),
    "Faction": "PLAYER"
}

EnemyBaseConfig = {
    "Position": (2000, 100),
    "Spritesheet": "enemy1",
    "Animation": {
        "enemy1-idle": Anim([], [(0, 0, 32, 32)], 0, 0.2, AnimationMode.LOOP)
    },
    "Size": (32, 32, 4),
    "Faction": "ENEMY"
}

class EntityConfig:
    __slots__ = (
        "Position",
        "Spritesheet",
        "Size",
        "Collider",
        "Animation"
    )

    def __init__(self, Position: tuple[int, int], Spritesheet, Size, Animation):
        self.Position = Position
        self.Spritesheet = Spritesheet
        self.Size = Size
        self.Animation = Animation




Asteriod1 = EntityConfig(
    Position = (-100, -100),
    Spritesheet = "Asteriod",
    Size = (32, 32),
    Animation = {
        "Asteriod-idle": Anim([], [(0, 0, 64, 64)], 0, 0.2, AnimationMode.LOOP)
    }
)




# ENEMIES

normal_EnemyConfig = {
            "Animation": {                
                "spritesheet": "enemy1",
                "animation": {
                    "enemy1-idle": Anim([], [(0,0,32,32)], 0, 0.2, AnimationMode.LOOP)
                },
            },
            "Position": (0,0),
            "Collider": (32,32),
            "Velocity": (50),
            "Cannon": (0.4),
            "Size": (32,32,1),
            "Health": (100)
        }