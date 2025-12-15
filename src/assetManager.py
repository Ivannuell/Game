from spritesheet import Spritesheet
import os


class AssetsManager:
    def __init__(self):
        self.assets = {}
        self.current_dir = os.path.dirname(__file__)
        self.assets_dir = os.path.join(
            os.path.dirname(self.current_dir), 'ship')
        # self.assets_dir = os.path.abspath(self.assets_dir)

    def load_assets(self):

        # Manually add's the asset should be done in the loading scene.
        player_spritesheet = os.path.join(
            self.assets_dir, 'Main Ship - Engines - Base Engine - Idle.png')
        
        obstacle = os.path.join(
            self.assets_dir, 'Main Ship - Base - Full health.png'
        )
        self.add_asset(player_spritesheet, 'booster')
        self.add_asset(obstacle, 'ship')

    def add_asset(self, asset, asset_key):
        self.assets[asset_key] = asset

    def get_asset(self, asset_key):
        return self.assets[asset_key]
