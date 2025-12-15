# This needs to refactored and make it a parent class for real entities on the game.

import pygame
from entities.animatedSprite import AnimatedSprite
from spritesheet import Spritesheet


class Entity:
    def __init__(self, game):
        self.game = game
        self.components = {}

    def add_component(self, component):
        self.components[component.id] = component

    def get_component(self, component_id):
        return self.components[component_id]
        # return self.components.get(component_id)    

    def has_component(self, component_id):
        return component_id in self.components

    def _init_Entity(self):
        self._build_Animation()
        self._build_Rect()

    def _build_Rect(self):
        if self.has_component('Collider'):
            col = self.get_component('Collider')
            scale = self.get_component("Animation").frame_scale

            col.width *= scale
            col.height *= scale

    def _build_Animation(self):
        animation = self.get_component("Animation")
        sprite = self.get_component("Sprite")

        spritesheet = Spritesheet(self.game.asset_manager.get_asset(animation.spritesheet), True)
        for key, anim in animation.anim.items():
            anim.frames = spritesheet.get_animation(anim.frame_coords, anim.frame_duration, scale=animation.frame_scale)
            anim.name = key
            animation.anim_list[anim.name] = anim.frames

            if animation.active_name == "":
                animation.active_anim = animation.anim_list[anim.name]
                animation.active_name = anim.name
                sprite.image = animation.active_anim.get_frame(0)

   

