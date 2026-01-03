from enum import Enum
import math

from components.components import *
from entities.entity import Entity

class SceneList(Enum):
    PAUSE = 0
    GAME = 1
    MAIN_MENU = 2
    PRELOAD = 3

ACCELERATION = 1200
FRICTION = 1000
SPRITE_FORWARD_OFFSET = -math.pi / 2
MIN_SPEED = 300


def get_Angle(source: Entity, target: Entity) -> float:
    if not source.has(Position) and not target.has(Position):
        raise Exception("Source and Target must have Position Component")
    
    dx = target.get(Position).x - source.get(Position).x
    dy = target.get(Position).y - source.get(Position).y
    
    return math.atan2(dy, dx)

def clamp_value(value, minimum, maximum): 
    return max(minimum, min(value, maximum))

def clamp_min_speed(vx, vy, min_speed):
    speed = math.hypot(vx, vy)
    if speed == 0 or speed >= min_speed:
        return vx, vy

    scale = min_speed / speed
    return vx * scale, vy * scale
