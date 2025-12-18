import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity

class Component:
    def __init__(self, id):
        self.id = id

class Anim:
    def __init__(self, frames, frame_coords, frame_index, frame_duration):
        self.name = ''
        self.frames = frames
        self.frame_coords = frame_coords
        self.frame_index = frame_index
        self.frame_duration = frame_duration

class Position(Component):
    def __init__(self, x, y):
        super().__init__("Position")
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, speed):
        super().__init__("Velocity")
        self.x = 0
        self.y = 0
        self.speed = speed

class Sprite(Component):
    def __init__(self, image=None):
        super().__init__("Sprite")
        self.image = image

class Animation(Component):
    def __init__(self, animation, spritesheet, frame_scale=1):
        super().__init__("Animation")
        self.anim = animation
        self.spritesheet = spritesheet
        self.active_anim = None
        self.active_name = ""
        self.active_frame: pygame.surface.Surface
        self.anim_list = {}
        self.frame_scale = frame_scale

class Collider(Component):
    def __init__(self, width, height, offset_x=0, offset_y=0):
        super().__init__("Collider")
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

class Projectile(Component):
    def __init__(self, faction):
        super().__init__("Projectile")
        self.faction = faction

class CollidedWith(Component):
    def __init__(self): 
        super().__init__("CollidedWith")
        self.entities: list[Entity] = []

# TAGS
class Solid(Component):
    def __init__(self):
        super().__init__("Solid")

class InputControlled(Component):
    def __init__(self):
        super().__init__("InputControlled")


class Ship(Component):
    def __init__(self):
        super().__init__("Ship")

class Cannon(Component):
    def __init__(self, cooldown):
        super().__init__("Cannon")
        self.cooldown = cooldown