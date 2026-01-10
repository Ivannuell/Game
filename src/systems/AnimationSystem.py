from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity

from registries.AnimationStateList import AnimationStateList
from helper import MIN_SPEED
from systems.system import System
from components.components import *

class Playback_AnimationSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if entity.has(Sprite, Animation, AnimationState):
                sprite = entity.get(Sprite)
                animation = entity.get(Animation)
                anim_state = entity.get(AnimationState)

                if anim_state.current != anim_state.previous:
                    if anim_state.current == AnimationStateList.IDLE:
                        animation.active_anim = animation.get_anim(animation.spritesheet + '-idle')
                    elif anim_state.current == AnimationStateList.MOVE:
                        animation.active_anim = animation.get_anim(animation.spritesheet + '-move')

                anim_state.previous = anim_state.current

                frame = animation.active_anim.get_frame(dt)
                sprite.image = frame
                sprite.original = frame


class State_AnimationSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if not entity.has(AnimationState):
                continue 

            if entity.has(Parent):
                parent_m = entity.get(Parent).entity.get(MovementIntent)
                state = entity.get(AnimationState)
                moving = False
                if parent_m.move_x != 0 and parent_m.move_y != 0:
                    moving = True
                else:
                    moving = False

                new_state = AnimationStateList.MOVE if moving else AnimationStateList.IDLE
                if state.current != new_state:
                    state.current = new_state #type: ignore

