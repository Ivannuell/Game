from typing import TYPE_CHECKING

from entities.system_Entities.animationPlayer import AnimationEvent

if TYPE_CHECKING:
    from entities.entity import Entity

from components.intents import AnimationPlayer, Play_CollisionImpact_Event
from registries.AnimationStateList import AnimationMode, AnimationStateList
from helper import MIN_SPEED
from systems.system import System
from components.components import *

class State_AnimationSystem(System):
    def __init__(self) -> None:
        super().__init__()

    def update(self, entities: 'list[Entity]', dt):
        for entity in entities:
            if not entity.has(AnimationState, Animation):
                continue 

            state = entity.get(AnimationState)
            state.current = AnimationStateList.IDLE

            if entity.has(AnimationPlayer):
                state = entity.get(AnimationState)
                state.locked = True
                state.current = AnimationStateList.IMPACT

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
                    match anim_state.current:
                        case AnimationStateList.IMPACT:
                            animation.active_anim = animation.get_anim(animation.spritesheet + '-impact')
                        case AnimationStateList.IDLE:
                            animation.active_anim = animation.get_anim(animation.spritesheet + '-idle')
                        case AnimationStateList.MOVE:
                            animation.active_anim = animation.get_anim(animation.spritesheet + '-move')

                anim_state.previous = anim_state.current

                if animation.active_anim is None:
                    continue

                frame = animation.active_anim.get_frame(dt)
                sprite.image = frame
                sprite.original = frame


class Events_AnimationSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    def update(self, entities: 'list[Entity]', dt):
        events: 'list[Entity]' = []
        for e in entities:
            if e.has(Play_CollisionImpact_Event):
                anim_pos = e.get(Play_CollisionImpact_Event)

                config = {
                    "Posx": anim_pos.pos_x,
                    "Posy": anim_pos.pos_y,
                    "Spritesheet": 'Explosion1',
                    "Animation": {
                        "Explosion1-impact": Anim([], [(0,0,32,32), (32,0,32,32), (64,0,32,32), (96,0,32,32), (128,0,32,32)], 0, 0.08, AnimationMode.NORMAL)
                    },
                    "AnimMode": AnimationMode.NORMAL
                }

                events.append(AnimationEvent(config, self.game))
                e.remove(Play_CollisionImpact_Event)

        entities.extend(events)


class EventCleanup_AnimationSystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game


    def update(self, entities: 'list[Entity]', dt):
        for e in entities:
            if e.has(Animation, AnimationPlayer):
                anim = e.get(Animation)

                if anim.active_anim is None:
                    continue

                if anim.active_anim.is_animation_finished():
                    e.add(Destroy())
            
                
