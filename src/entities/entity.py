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

   

