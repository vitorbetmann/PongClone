import pygame


class Scoreboard:
    def __init__(self, game):
        self.window = game.window
        self.window_rect = self.window.get_rect()

        self.p1_score = self.p2_score = 0
        self.color = game.settings.scoreboard_color
        self.font_size = game.settings.SCOREBOARD_FONT_SIZE
        score_text = f"{self.p1_score} PONG {self.p2_score}"
        self.score_surface = pygame.font.SysFont(None, self.font_size).render(
            score_text, False, self.color
        )
        self.score_rect = self.score_surface.get_rect()
        self.score_rect.midtop = self.window_rect.midtop
        self.score_rect.y += 20

    def draw_score(self):
        self.window.blit(self.score_surface, self.score_rect)

    def draw_division(self):
        current_y = self.score_rect.height * 2
        while current_y < self.window_rect.height:
            new_rect = pygame.Rect(self.window_rect.centerx, current_y, 10, 40)
            pygame.draw.rect(self.window, "white", new_rect)
            current_y += new_rect.height * 2

    def draw_text(self, text, shift=0, font_size=70):
        text_surface = pygame.font.SysFont(None, font_size).render(
            text, False, self.color
        )
        text_rect = text_surface.get_rect()
        text_rect.center = self.window_rect.centerx, self.window_rect.centery + shift
        self.window.blit(text_surface, text_rect)

    def update(self):
        score_text = f"{self.p1_score}  PONG  {self.p2_score}"
        self.score_surface = pygame.font.SysFont(None, self.font_size).render(
            score_text, False, self.color
        )

    def reset(self):
        self.p1_score = self.p2_score = 0
