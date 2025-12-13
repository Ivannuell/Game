import pygame

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
    def __init__(self, dx, dy):
        super().__init__("Velocity")
        self.dx = dx
        self.dy = dy

class Sprite(Component):
    def __init__(self, image=None):
        super().__init__("Sprite")
        self.image = image

class Animation(Component):
    def __init__(self, animation, spritesheet):
        super().__init__("Animation")
        self.anim = animation
        self.spritesheet = spritesheet
        self.active_anim = None
        self.active_name = ""
        self.active_frame: pygame.surface.Surface
        self.anim_list = {}


class Collider(Component):
    def __init__(self, shape):
        super().__init__("Collider")
        self.shape = shape