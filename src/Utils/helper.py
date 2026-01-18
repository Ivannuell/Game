from enum import Enum
import math


ACCELERATION = 1200
FRICTION = 1000
ENEMY_ACCELARATION = 1000

SPRITE_FORWARD_OFFSET = -math.pi / 2
MIN_SPEED = 100

ROTATION_SMOOTHNESS = 9

ROT_SPEED = 0.4

def clamp_value(value, minimum, maximum): 
    return max(minimum, min(value, maximum))

def clamp_min_speed(vx, vy, min_speed):
    speed = math.hypot(vx, vy)
    if speed == 0 or speed >= min_speed:
        return vx, vy

    scale = min_speed / speed
    return vx * scale, vy * scale


def move_towards(current, target, max_delta):
    if current < target:
        return min(current + max_delta, target)
    if current > target: 
        return max(current - max_delta, target)
    return target

def lerp_angle(current, target, t):
    """
    current, target: degrees
    t: 0..1 (interpolation factor)
    """
    delta = (target - current + 180) % 360 - 180
    return current + delta * t
