import pygame
import sys

from registries.AnimationStateList import AnimationMode


class Spritesheet:
    def __init__(self, filename, bg=None):
        self.image = pygame.image.load(filename)
        self.bg = bg
        self.image = self.image.convert_alpha()

    def get_image(self, frame, flip=False, scale=1.0):
        sprite = self.image.subsurface(frame)

        if flip:
            sprite = pygame.transform.flip(sprite, True, False)

        if scale > 1:
            sprite = pygame.transform.scale(
                sprite, (frame[2] * scale, frame[3] * scale))

        if self.bg != None:
            sprite.set_colorkey('black')

        return sprite

    def get_animation(self, frame_coords, frame_duration, scale=1.0, mode:AnimationMode|None = None):
        if len(frame_coords) == 1:
            frame = [self.get_image(frame_coords[0], scale=scale)]
            return _Anim(frame, frame_duration, mode)

        frames = [self.get_image(coords, scale=scale)
                  for coords in frame_coords]
        return _Anim(frames, frame_duration, mode)


# Animations still only supports looping ones
class _Anim:
    def __init__(self, frames, frame_duration, mode):
        self.frames = frames
        self.frame_duration = frame_duration
        self.animation_duration = self.frame_duration * len(self.frames)
        self.state_time: float = 0
        self.mode = mode

    def get_frame(self, delta_time):
        frame_index = self.get_frame_index(delta_time)
        return self.frames[frame_index]

    def get_first_frame(self):
        return self.frames[0]
    
    def get_last_frame(self):
        return self.frames[-1]
    
    def reset_time(self):
        self.state_time = 0.0

    def get_frame_index(self, delta_time):
        if len(self.frames) <= 1:
            return 0
        

        # if self.state_time >= self.animation_duration:
        #     self.state_time = 0

        self.state_time += delta_time
        frame_number = int(self.state_time/self.frame_duration)

        if self.mode == AnimationMode.NORMAL:
            frame_number = min(len(self.frames) - 1, frame_number)
        elif self.mode == AnimationMode.LOOP:
            frame_number = frame_number % len(self.frames)
        return frame_number

    def is_animation_finished(self):
        frame_number = int(self.state_time/self.frame_duration)
        return len(self.frames) - 1 < frame_number
