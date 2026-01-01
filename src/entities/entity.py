# This needs to refactored and make it a parent class for real entities on the game.

from spritesheet import Spritesheet
from typing import TYPE_CHECKING, Type, TypeVar
from components.components import *

T = TypeVar("T", bound=Component)

if TYPE_CHECKING:
    from baseGame import BaseGame
    from components.components import Component

class Entity:
    def __init__(self):
        self.game: "BaseGame"
        self.components: "dict[type, Component]" = {}

    def add(self, component):
        if self.components is None:
            return
        
        self.components[type(component)] = component
        return self

    def get(self, component_cls: Type[T]) -> T:
        return self.components[component_cls] # type: ignore

    def has(self, *component_classes: Type[T]):
        if not component_classes:
            raise ValueError("has() requires at least one component class")

        if not self.components:
            return False

        return all(comp in self.components for comp in component_classes)


    def remove(self, component_cls):
        self.components.pop(component_cls, None)

    def init_Entity(self):
        if self.has(Zoom):
            return
        self._build_Animation()
        self._build_Rect()

    def _build_Rect(self):
        if self.has(Collider):
            col = self.get(Collider)
            size = self.get(Size)

            if col.width is None or col.height is None:
                col.width = size.width
                col.height = size.height

    def _build_Animation(self):
        animation = self.get(Animation)
        sprite = self.get(Sprite)
        scale = self.get(Size)

        spritesheet = self.game.asset_manager.get_spritesheet(animation.spritesheet)
        for key, anim in animation.anim.items():
            anim.frames = spritesheet.get_animation(anim.frame_coords, anim.frame_duration, scale=scale.scale)
            anim.name = key
            animation.anim_list[anim.name] = anim.frames

            if animation.active_name == "":
                animation.active_anim = animation.anim_list[anim.name]
                animation.active_name = anim.name
                sprite.image = animation.active_anim.get_frame(0)

   

