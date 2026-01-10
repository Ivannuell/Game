from enum import Enum
from functools import lru_cache
import pygame


from typing import TYPE_CHECKING

from helper import SPRITE_FORWARD_OFFSET


if TYPE_CHECKING:
    from entities.entity import Entity
    from spritesheet import _Anim
    from entities.Spawn_Patterns.EnemyPatterns import SpawnPattern

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

class CommandType(Enum):
    CHANGE_SCENE = 1
    EXIT = 2
    PAUSE = 3
    RESUME = 4
    RESTART = 5

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
        self.anim_list = {}
        self.spritesheet = spritesheet
        self.active_anim : _Anim
        self.active_name = ""
        self.active_frame: pygame.surface.Surface

    def get_anim(self, anim_name):
        try:
            return self.anim_list[anim_name]
        except:
            return self.active_anim
        
@ComponentRegistry.register
class AnimationState(Component):
    def __init__(self):
        super().__init__()
        self.current = 0
        self.previous = 0
        self.locked = False

@ComponentRegistry.register
class Position(Component):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def set(self, position: pygame.Vector2):
        self.x = position.x
        self.y = position.y

class ViewPosition(Component):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0

@ComponentRegistry.register
class Parent(Component):
    def __init__(self) -> None:
        super().__init__()
        self.entity: Entity

class OffsetPosition(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y


@ComponentRegistry.register
class Velocity(Component):
    def __init__(self, speed = 0):
        super().__init__()
        self.x: float = 0
        self.y: float = 0
        self.speed = speed

@ComponentRegistry.register
class Sprite(Component):
    def __init__(self, image: pygame.Surface | None = None):
        super().__init__()
        self.image: pygame.Surface = image # type: ignore
        self.original: pygame.Surface = image # type: ignore

@ComponentRegistry.register
class Size(Component):
    def __init__(self, width, height, scale=1.0):
        super().__init__()
        self.scale: float = scale
        self.width = width * scale
        self.height = height * scale

@ComponentRegistry.register
class Collider(Component):
    def __init__(self, width=None, height=None):
        super().__init__()
        self.width: int | None = width
        self.height: int | None = height

@ComponentRegistry.register
class Projectile(Component):
    def __init__(self):
        super().__init__()
        self.faction = ""
        self.timeout = 1
        

    def reset(self):
        self.timeout = 1

@ComponentRegistry.register
class DamageEvent(Component):
    def __init__(self, amount=0, source=""):
        super().__init__()
        self.amount = amount
        self.source = source

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
        self.time_left = 0

@ComponentRegistry.register
class CollisionIdentity(Component):
    def __init__(self, role: str, layer: list[CollisionID], mask: list[CollisionID]):
        super().__init__()
        self.role = role
        self.layer: list[CollisionID] = layer
        self.mask: list[CollisionID] = mask


@ComponentRegistry.register
class UiElement(Component):
    def __init__(self) -> None:
        super().__init__()

class SystemEntity(Component):
    def __init__(self) -> None:
        super().__init__()


@ComponentRegistry.register
class PointerState(Component):
    def __init__(self):
        super().__init__()
        self.hovering = False

        # entity-specific press ownership
        self.pressed = False  

        # one-frame events
        self.entered = False
        self.exited = False
        self.clicked = False
        self.released = False

    def reset_frame(self):
        self.entered = False
        self.exited = False
        self.clicked = False
        self.released = False

class Orbit(Component):
    def __init__(self, center, radius, speed, angle=0):
        super().__init__()
        self.center = center      # Entity reference
        self.radius = radius
        self.speed = speed        # radians/sec
        self.angle = angle

class Rotation(Component):
    def __init__(self) -> None:
        super().__init__()
        self.rad_angle: float = 0
        self.target_angle: float = 0
        self.smoothing = 9
        self.set_target()

    def set_target(self):
        self.target_angle -= SPRITE_FORWARD_OFFSET



@ComponentRegistry.register
class FactionIdentity(Component):
    def __init__(self, faction = ""):
        super().__init__()
        self.faction = faction
        self.owner: Entity | None = None

@ComponentRegistry.register
class MovementIntent(Component):
    def __init__(self):
        super().__init__
        self.move_x = 0
        self.move_y = 0

    def reset(self):
        self.move_x = 0
        self.move_y = 0

@ComponentRegistry.register   
class FireIntent(Component):
    def __init__(self):
        super().__init__
        self.fired = False

@ComponentRegistry.register
class Clickable(Component):
    def __init__(self, buttonID) -> None:
        super().__init__()
        self.buttonID = buttonID


@ComponentRegistry.register
class Command(Component):
    def __init__(self, type: CommandType, payload=None) -> None:
        super().__init__()
        self.type = type
        self.payload = payload


@ComponentRegistry.register
class EnemyIntent(Component):
    def __init__(self) -> None:
        super().__init__()
        self.move = "LEFT"
        self.shoot = False

@ComponentRegistry.register
class Zoom(Component):
    def __init__(self) -> None:
        super().__init__()
        self.zoom = 1.0
        self.target_zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        self.zoom_step = 1.1
        
@ComponentRegistry.register
class EnemySpawner(Component):
    def __init__(self, pattern) -> None:
        super().__init__()
        self.pattern: 'SpawnPattern' = pattern


@ComponentRegistry.register
class Destroy(Component):
    def __init__(self) -> None:
        super().__init__()