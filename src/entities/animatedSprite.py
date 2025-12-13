import pygame
from spritesheet import Animation

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(groups)
        self.animation_list = {}
        self.active_anim: Animation
        self.active_name: str = ""
        self.elapsed_time = 0
        

    def add_animaton(self, animation, name):
        self.animation_list[name] = animation

        if self.active_name == "":
            self.set_active_animation(name)


    def set_active_animation(self, animation_name):
        if not self.animation_list[animation_name]:
            print("Animation does not exist yet")
            return

        self.active_name = animation_name
        self.active_anim = self.animation_list[self.active_name]
        self.elapsed_time = 0

    def get_animation(self, animation_name):
        return self.animation_list[animation_name]

            
    def update(self, delta_time):
        self.elapsed_time += delta_time        
