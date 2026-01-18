import pygame

class DebugOverlaySystem:
    def __init__(self, profiler, font_size=14):
        self.profiler = profiler
        self.enabled = False

        self.font = pygame.font.SysFont("consolas", font_size)
        self.line_height = font_size + 4

        self.cached_surfaces = {}
        self.frame_counter = 0
        self.update_interval = 10  # update text every N frames

    def toggle(self):
        self.enabled = not self.enabled

    def update(self):
        if not self.enabled:
            return

        self.frame_counter += 1
        if self.frame_counter % self.update_interval != 0:
            return

        stats = self.profiler.stats()
        self.cached_surfaces.clear()

        for name, data in stats.items():
            text = f"{name:<25} {data['avg']:6.2f} ms  max {data['max']:6.2f}"
            self.cached_surfaces[name] = self.font.render(
                text, True, (0, 255, 0)
            )

    def render(self, screen):
        if not self.enabled:
            return

        y = 10
        for surf in self.cached_surfaces.values():
            screen.blit(surf, (10, y))
            y += self.line_height
