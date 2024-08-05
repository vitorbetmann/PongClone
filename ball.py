import random

import pygame
from pygame.rect import Rect


class Ball(Rect):
    def __init__(self, game):
        self.window = game.window
        self.window_rect = self.window.get_rect()
        self.ball_width = self.ball_height = game.settings.BALL_SIDE_LENGTH
        self.starting_x = self.window.get_rect().centerx - self.ball_width / 2
        self.starting_y = self.window.get_rect().centery - self.ball_height / 2

        super().__init__(
            self.starting_x,
            self.starting_y,
            self.ball_width,
            self.ball_height,
        )

        self.color = game.settings.ball_color
        self.x_speed = game.settings.BALL_X_SPEED * random.choice([-1, 1])
        self.y_speed = game.settings.BALL_Y_SPEED * random.choice([-1, 1])

        self.wall_hit_sound = pygame.mixer.Sound("sounds/wall_hit.wav")

    def draw(self):
        pygame.draw.rect(self.window, self.color, self)

    def update_pos(self):
        if self.top <= 0 or self.bottom >= self.window_rect.height:
            self.wall_hit_sound.play()
            self.invert_y_direction()

        self.x += self.x_speed
        self.y += self.y_speed

    def reset(self):
        self.x_speed *= -1
        self.y_speed *= random.choice([-1, 1])
        self.center = self.window_rect.center

    def invert_x_direction(self):
        self.x_speed *= -1

    def invert_y_direction(self):
        self.y_speed *= -1

    def is_moving_right(self):
        return self.x < self.x + self.x_speed

    def is_moving_left(self):
        return not self.is_moving_right()
