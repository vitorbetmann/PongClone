import pygame
from pygame.rect import Rect


class Paddle(Rect):
    def __init__(self, game, pos, name):
        self.name = name
        self.window = game.window
        self.window_rect = self.window.get_rect()
        self.FPS = game.settings.FPS

        self.speed = game.settings.PADDLE_SPEED

        self.color = game.settings.paddle_color
        self.initial_pos = pos
        self.left, self.top = self.initial_pos
        self.width = game.settings.PADDLE_WIDTH
        self.height = game.settings.PADDLE_HEIGHT
        super().__init__(self.left, self.top, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self)

    def move_up(self):
        self.top = max(0, self.top - self.speed)

    def move_down(self):
        self.bottom = min(self.window_rect.height, self.bottom + self.speed)

    def slowly_move_up(self):
        self.top = max(0, self.top - int(self.speed / 4))

    def slowly_move_down(self):
        self.bottom = min(self.window_rect.height, self.bottom + int(self.speed / 4))

    def reset(self):
        self.left, self.top = self.initial_pos
