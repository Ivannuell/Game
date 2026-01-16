from components.components import *
from entities.entity import Entity
from systems.system import System


class HealthBar_DisplaySystem(System):
    def __init__(self, game) -> None:
        super().__init__()
        game_screen = game.screen.display_surface
        game_screen_rect = game_screen.get_rect()
        
        self.tiny_font = pygame.font.Font(None, 15)
        self.health_bar_con = pygame.Rect(30, game_screen_rect.height - 50, 300, 20)
        self.health_bar = self.health_bar_con.copy()
        self.health_bar_con.size = (self.health_bar_con.width + 3, self.health_bar_con.height + 3)
        self.health_bar_con.y -= 1.5

        self.health_con = self.health_bar_con.width / 100


    def render(self, entities: list[Entity], screen):
        for entity in entities:
            if entity.has(HeadQuarter):
                health = entity.get(Health)

                self.health_bar.width = self.health_con * (health.health / 100) * 10

                health_text = self.tiny_font.render(f"{health.health}/{health.full_health}", False, 'white')
                pygame.draw.rect(screen.display_surface, 'red', self.health_bar, 0, 5)
                pygame.draw.rect(screen.display_surface, 'white', self.health_bar_con, 1, 5)
                screen.display_surface.blit(health_text, (self.health_bar_con.x + 20, self.health_bar_con.y - 10))
