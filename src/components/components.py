from abc import ABC, abstractmethod, abstractproperty
from enum import Enum, auto
from functools import lru_cache
import math
import pygame


from typing import TYPE_CHECKING

from Utils.helper import SPRITE_FORWARD_OFFSET
from registries.AnimationStateList import AnimationStateList
from registries.EnemyList import EnemyActions


if TYPE_CHECKING:
    from entities.entity import Entity
    from Utils.spritesheet import _Anim
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
    Players = auto()
    Enemies = auto()
    Projectiles = auto()
    Obstacles = auto()
    Farm = auto()

class CommandType(Enum):
    CHANGE_SCENE = auto()
    EXIT = auto()
    PAUSE = auto()
    RESUME = auto()
    RESTART = auto()

class Anim:
    def __init__(self, frames, frame_coords, frame_index, frame_duration, mode):
        self.name: str = ''
        self.frames = frames
        self.frame_coords = frame_coords
        self.frame_index = frame_index
        self.frame_duration = frame_duration
        self.mode = mode

class Component(ABC):
    pass

@ComponentRegistry.register
class Animation(Component):
    def __init__(self, animation, spritesheet):
        super().__init__()
        self.anim: dict[str, Anim] = animation
        self.anim_list = {}
        self.spritesheet = spritesheet
        self.active_anim : _Anim
        self.previous_anim: _Anim
        self.active_name = ""
        self.active_frame: pygame.surface.Surface

    def get_anim(self, anim_action):
        try:
            return self.anim_list[anim_action]
        except:
            # raise Exception(f'No animation {anim_action}')
            print(f"{anim_action} is not defined")
            return self.anim_list[f"{self.spritesheet}-idle"]
        
    def reset_timers(self):
        for key, anim in self.anim_list.items():
            anim.reset_time()
        
@ComponentRegistry.register
class AnimationState(Component):
    def __init__(self):
        super().__init__()
        self.current: AnimationStateList = 0 # type: ignore
        self.previous: AnimationStateList | None = None # type: ignore
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
class CollidedWith(Component):
    def __init__(self): 
        super().__init__()
        self.entities: list[Entity] = []

@ComponentRegistry.register
class Health(Component):
    def __init__(self, health):
        super().__init__()
        self.health = health
        self.full_health = health

@ComponentRegistry.register
class Damage(Component):
    def __init__(self, damage):
        super().__init__()
        self.damage = damage

@ComponentRegistry.register
class DamageEvent(Component):
    def __init__(self, amount=0, source:'Entity|None'=None):
        super().__init__()
        self.amount = amount
        self.source = source

@ComponentRegistry.register
class Static(Component):
    def __init__(self):
        super().__init__()

@ComponentRegistry.register
class HeadQuarter(Component):
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
@ComponentRegistry.register
class UtilityEntity(Component):
    def __init__(self) -> None:
        super().__init__()

@ComponentRegistry.register
class GridCell(Component):
    def __init__(self) -> None:
        super().__init__()
        self.cell = set()

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
        self.angle: float = 0
        self.angleOfAttack: float = 0
        self.angular_vel = 0 
        self.smoothing = 9
        self.visual_deg = math.degrees(self.angle)
        # self.set_target()

    def set_target(self):
        self.angleOfAttack -= SPRITE_FORWARD_OFFSET



@ComponentRegistry.register
class FactionIdentity(Component):
    def __init__(self, faction = ""):
        super().__init__()
        self.faction = faction
        self.owner: Entity | None = None

@ComponentRegistry.register
class MovementIntent(Component):
    def __init__(self):
        super().__init__()
        self.move_x = 0
        self.move_y = 0
        self.rotate_left = False
        self.rotate_right = False

    def reset(self):
        self.move_x = 0
        self.move_y = 0
        self.rotate_left = False
        self.rotate_right = False

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
        self.current_action = EnemyActions.Attacking
        self.previous_action = EnemyActions.Invading
        self.special_action = None
        self.radar_range = 7


@ComponentRegistry.register
class Target(Component):
    def __init__(self, target) -> None:
        super().__init__()
        self.prev_target = target
        self.target = target
        self.Main_target = target
    

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
class AsteriodSpawner(Component):
    def __init__(self) -> None:
        super().__init__()
        

@ComponentRegistry.register
class ZoneComponent(Component):
    def __init__(self,id, maxcount, pos, size) -> None:
        super().__init__()
        self.maxCount = maxcount
        self.count = 0
        self.pos = pos
        self.size = size
        self.id = id

@ComponentRegistry.register
class ZoneId(Component):
    def __init__(self, id) -> None:
        super().__init__()
        self.id = id

class FarmDestroyed(Component):
    def __init__(self, idm) -> None:
        super().__init__()
        self.id = idm


@ComponentRegistry.register
class Destroy(Component):
    def __init__(self) -> None:
        super().__init__()

@ComponentRegistry.register   
class ShootIntent(Component):
    def __init__(self):
        super().__init__
        self.fired = False

@ComponentRegistry.register   
class Attacker(Component):
    def __init__(self):
        super().__init__

@ComponentRegistry.register   
class Farmer(Component):
    def __init__(self):
        super().__init__

@ComponentRegistry.register
class Cannon(Component):
    def __init__(self, cooldown):
        self.time_left = 0
        self._cooldowntime_ = cooldown

    def cooldown(self):
        if self.time_left >= self._cooldowntime_: return True
        else: return False

@ComponentRegistry.register
class ManualAim(Component):
    def __init__(self, angle) -> None:
        self.angleOfAttack = angle

@ComponentRegistry.register
class AutoAim(Component):
    def __init__(self, range) -> None:
        self.range = range


@ComponentRegistry.register
class Gold(Component):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount
        
@ComponentRegistry.register
class GoldContainer(Component):
    def __init__(self, capacity):
        super().__init__()
        self.gold = 0
        self.gold_capacity = capacity

@ComponentRegistry.register
class EarnGoldEvent(Component):
    def __init__(self, amount=0, source:'Entity | None'=None):
        super().__init__()
        self.amount = amount
        self.source = source

@ComponentRegistry.register
class Farm(Component):
    def __init__(self):
        super().__init__()

@ComponentRegistry.register
class IsDead(Component):
    def __init__(self):
        super().__init__()

@ComponentRegistry.register
class HitBy(Component):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity

@ComponentRegistry.register
class Vision(Component):
    def __init__(self, visual_range):
        super().__init__()
        self.range = visual_range

@ComponentRegistry.register
class Perception(Component):
    def __init__(self):
        super().__init__()
        self.visible_entities: 'list[Entity] | list[Entity, float]' = []
        self.cooldown = 0.0
