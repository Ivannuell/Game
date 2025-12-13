# config.py
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class AnimationConfig:
    spritesheet: str = ""
    spritesheet_bg: bool = False
    frame_coords: Tuple[tuple, ...] = field(default_factory=tuple)
    animation_name: str = ""
    frame_duration: float = 0.1


@dataclass
class PlayerShipConfig:
    animation: AnimationConfig = field(default_factory=AnimationConfig)
