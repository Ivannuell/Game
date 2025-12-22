from enum import Enum
import pygame


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.entity import Entity
    from spritesheet import _Anim

class ComponentRegistry:
    _components = {}

    @classmethod
    def register(cls, component_cls):
        cls._components[component_cls] = component_cls.__name__
        return component_cls

    @classmethod
    def id_of(cls, component_cls):
        return cls._components[component_cls]

class CollisionID(Enum):
    Players = 0
    Enemies = 1
    Projectiles = 2
    Obstacles = 3

class Anim:
    def __init__(self, frames, frame_coords, frame_index, frame_duration):
        self.name: str = ''
        self.frames = frames
        self.frame_coords = frame_coords
        self.frame_index = frame_index
        self.frame_duration = frame_duration

class Component:
    pass

@ComponentRegistry.register
class Animation(Component):
    def __init__(self, animation, spritesheet):
        super().__init__()
        self.anim = animation
        self.spritesheet = spritesheet
        self.active_anim : _Anim
        self.active_name = ""
        self.active_frame: pygame.surface.Surface
        self.anim_list = {}

@ComponentRegistry.register
class Position(Component):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

@ComponentRegistry.register
class Velocity(Component):
    def __init__(self, speed):
        super().__init__()
        self.x = 0
        self.y = 0
        self.speed = speed

@ComponentRegistry.register
class Sprite(Component):
    def __init__(self, image: pygame.Surface | None = None):
        super().__init__()
        self.image: pygame.Surface = image # type: ignore

@ComponentRegistry.register
class Size(Component):
    def __init__(self, width, height, scale=1):
        super().__init__()
        self.scale = scale
        self.width = width * scale
        self.height = height * scale

@ComponentRegistry.register
class Collider(Component):
    def __init__(self):
        super().__init__()
        self.width: int
        self.height: int

@ComponentRegistry.register
class Projectile(Component):
    def __init__(self, faction):
        super().__init__()
        self.faction = faction

@ComponentRegistry.register
class CollidedWith(Component):
    def __init__(self): 
        super().__init__()
        self.entities: list[Entity] = []

@ComponentRegistry.register
class Health(Component):
    def __init__(self, health):
        super().__init__()
        self.health = health

@ComponentRegistry.register
class Damage(Component):
    def __init__(self, damage):
        super().__init__()
        self.damage = damage

@ComponentRegistry.register
class Solid(Component):
    def __init__(self):
        super().__init__()

@ComponentRegistry.register
class InputControlled(Component):
    def __init__(self):
        super().__init__()

@ComponentRegistry.register
class Ship(Component):
    def __init__(self):
        super().__init__()

@ComponentRegistry.register
class Cannon(Component):
    def __init__(self, cooldown):
        super().__init__()
        self.cooldown = cooldown

@ComponentRegistry.register
class CollisionIdentity(Component):
    def __init__(self, layer: list[CollisionID], mask: list[CollisionID]):
        super().__init__()
        self.layer: list[CollisionID] = layer
        self.mask: list[CollisionID] = mask

@ComponentRegistry.register
class FactionIdentity(Component):
    def __init__(self, faction):
        super().__init__()
        self.faction = faction

@ComponentRegistry.register
class MovementIntent(Component):
    def __init__(self):
        self.move_x = 0
        self.move_y = 0

@ComponentRegistry.register   
class FireIntent(Component):
    def __init__(self):
        self.fired = False