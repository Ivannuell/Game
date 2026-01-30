import pygame
import os

from Utils.spritesheet import Spritesheet


class AssetsManager:
    def __init__(self):
        self.assets: 'dict[str, Spritesheet]' = {}
        self.current_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(os.path.dirname(self.current_dir), '../Assets')

    def load_assets(self):

        # Manually add's the asset should be done in the loading scene.
        booster = os.path.join(
            self.assets_dir, 'booster.png')
        
        ship = os.path.join(
            self.assets_dir, 'Ship1.png'
        )
        
        bullet = os.path.join(
            self.assets_dir, 'Projectile01.png'
        )

        assteriod = os.path.join(self.assets_dir, 'Asteroids-Sheet.png')
        enemy1 = os.path.join(self.assets_dir, 'fighter1.png')
        explosion = os.path.join(self.assets_dir, 'Explosion01-Sheet.png')
        # player = os.path.join(self.assets_dir, 'Ship1.png')
        player_cannon = os.path.join(self.assets_dir, 'Main Ship - Weapons - Auto Cannon.png')
        player = os.path.join(self.assets_dir, 'Player01-Sheet.png')
        
        self.add_asset('booster', Spritesheet(booster))
        self.add_asset('ship', Spritesheet(ship))
        self.add_asset('bullet', Spritesheet(bullet))
        self.add_asset('enemy1', Spritesheet(enemy1))
        self.add_asset('projectile', pygame.image.load(bullet).convert_alpha())
        self.add_asset('Explosion1', Spritesheet(explosion))
        self.add_asset('Asteriod', Spritesheet(assteriod))
        self.add_asset('player', Spritesheet(player))
        self.add_asset('player_cannon', Spritesheet(player_cannon))

    def add_asset(self, asset_key, asset):
        self.assets[asset_key] = asset

    def get_asset(self, asset_key) -> Spritesheet | pygame.Surface:
        return self.assets[asset_key]

    def get_spritesheet(self, key) -> Spritesheet:
        return self.assets[key]
