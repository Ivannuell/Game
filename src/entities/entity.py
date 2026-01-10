
from typing import TYPE_CHECKING, Type, TypeVar
from components.components import *


if TYPE_CHECKING:
    from baseGame import BaseGame
    from components.components import Component
T = TypeVar("T", bound=Component)



class Entity:
    def __init__(self):
        self.game: "BaseGame"
        self.components: "dict[type, Component]" = {}
        self.__qualname__ = "Entity"

    def add(self, component):
        if self.components is None:
            return
        
        if self.has(component):
            self.components.pop(type(component))
        
        self.components[type(component)] = component
        return self

    def get(self, component_cls: Type[T]) -> T:
        return self.components[component_cls] # type: ignore

    def has(self, *component_classes: Type[T]):
        if not component_classes:
            raise ValueError("has() requires at least one component class")

        return all(comp in self.components for comp in component_classes)


    def remove(self, component_cls):
        self.components.pop(component_cls, None)

    def init_Entity(self):
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
        if not self.has(Animation):
            return
        
        animation = self.get(Animation)
        sprite = self.get(Sprite)
        scale = self.get(Size)

        spritesheet = self.game.asset_manager.get_spritesheet(animation.spritesheet)

        for key, anim in animation.anim.items():
            anim.frames = spritesheet.get_animation(anim.frame_coords, anim.frame_duration, scale=scale.scale)
            anim.name = key
            animation.anim_list[anim.name] = anim.frames
            
            if sprite.image is None or animation.active_name == "":
                sprite.image = anim.frames.get_first_image()

            if animation.active_name == "":
                animation.active_anim = anim.frames
                animation.active_name = anim.name

   

