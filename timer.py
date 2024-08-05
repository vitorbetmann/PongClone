from pygame.font import SysFont


class Timer:
    def __init__(self, game, text):
        self.window = game.window
        self.countdown_surface = SysFont(None, 200).render(text, False, "white")
        self.countdown_rect = self.countdown_surface.get_rect()
        self.countdown_rect.center = self.window.get_rect().center

    def draw(self):
        self.window.blit(self.countdown_surface, self.countdown_rect)
