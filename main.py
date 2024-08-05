import sys

import pygame
from pygame.locals import *

import timer
from ball import Ball
from paddle import Paddle
from pong_ai import PongAi
from scoreboard import Scoreboard
from settings import Settings


class Pong:
    STATE_START = "start"
    STATE_PAUSE = "pause"
    STATE_PLAYING = "playing"
    STATE_COUNTDOWN = "countdown"
    STATE_GAME_OVER = "game over"

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.window = pygame.display.set_mode(
            (self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Pong")
        pygame.display.set_icon(pygame.image.load("images/pong_icon.png"))
        self.window_rect = self.window.get_rect()
        self.clock = pygame.time.Clock()

        self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        self.paddle_hit_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")

        self.bg_color = self.settings.bg_color

        self.scoreboard = Scoreboard(self)

        self.paddle_1 = Paddle(
            self,
            (
                self.settings.PADDLE_WIDTH * self.settings.PADDLE_OFFSET,
                (self.settings.WINDOW_HEIGHT - self.settings.PADDLE_HEIGHT) / 2,
            ),
            "paddle 1",
        )
        self.paddle_2 = Paddle(
            self,
            (
                self.settings.WINDOW_WIDTH
                - self.settings.PADDLE_WIDTH * self.settings.PADDLE_OFFSET,
                (self.settings.WINDOW_HEIGHT - self.settings.PADDLE_HEIGHT) / 2,
            ),
            "paddle 2",
        )
        self.player_paddle = self.paddle_1

        self.ball = Ball(self)

        self.ai = PongAi(self)

        self.game_state = Pong.STATE_START
        self.previous_state = None
        self.delta_time_start = None
        self.timer = None

    def run(self):
        while True:
            self._check_for_events()

            if (
                self.game_state is not Pong.STATE_PAUSE
                and self.game_state is not Pong.STATE_START
            ):
                self._check_keys_pressed()
                self.ai.predict_move()

                if self.game_state == Pong.STATE_PLAYING:
                    self._playing_state_logic()
                elif self.game_state == Pong.STATE_COUNTDOWN:
                    self._countdown_state_logic()

            self._draw_all()
            pygame.display.update()
            self.clock.tick(self.settings.FPS)

    def _reset_all(self):
        self.ball.reset()
        self.paddle_1.reset()
        self.paddle_2.reset()
        self.scoreboard.reset()
        self.scoreboard.update()

    def _check_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (
                event.key == K_RETURN or event.key == K_KP_ENTER
            ):
                match self.game_state:
                    case Pong.STATE_START:
                        self.delta_time_start = pygame.time.get_ticks()
                        self.game_state = Pong.STATE_COUNTDOWN
                    case Pong.STATE_PLAYING:
                        self.previous_state = self.game_state
                        self.game_state = Pong.STATE_PAUSE
                    case Pong.STATE_COUNTDOWN:
                        self.previous_state = self.game_state
                        self.game_state = Pong.STATE_PAUSE
                    case Pong.STATE_PAUSE:
                        if self.previous_state == Pong.STATE_COUNTDOWN:
                            self.delta_time_start = pygame.time.get_ticks()
                            self.game_state = Pong.STATE_COUNTDOWN
                        else:
                            self.game_state = Pong.STATE_PLAYING
                        self.previous_state = Pong.STATE_PAUSE
                    case Pong.STATE_GAME_OVER:
                        self._reset_all()
                        self.delta_time_start = pygame.time.get_ticks()
                        self.previous_state = self.game_state
                        self.game_state = Pong.STATE_COUNTDOWN

    def ball_hit_paddle(self):
        if pygame.Rect.colliderect(self.ball, self.paddle_1):
            self.ball.left = self.paddle_1.right
            self.ball.invert_x_direction()
            self.paddle_hit_sound.play()

        elif pygame.Rect.colliderect(self.ball, self.paddle_2):
            self.ball.right = self.paddle_2.left
            self.ball.invert_x_direction()
            self.paddle_hit_sound.play()

    def _is_score(self):
        if self.ball.left <= 0:
            self.scoreboard.p2_score += 1
            return True
        if self.ball.right >= self.window_rect.width:
            self.scoreboard.p1_score += 1
            return True
        return False

    def _check_keys_pressed(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w]:
            self.player_paddle.move_up()
        if pressed_keys[K_s]:
            self.player_paddle.move_down()

    def _playing_state_logic(self):
        self.ball.update_pos()
        if self.ball_hit_paddle():
            self.ball.invert_x_direction()

        if self._is_score():
            self.score_sound.play()
            self.ball.reset()
            self.scoreboard.update()
            self.delta_time_start = pygame.time.get_ticks()
            self.game_state = self.STATE_COUNTDOWN

        if self._is_game_over():
            self.game_state = Pong.STATE_GAME_OVER

    def _countdown_state_logic(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.delta_time_start
        countdown_str = str(3 - int(delta_time / 1000))
        self.timer = timer.Timer(self, countdown_str)

        if delta_time >= 3000:
            self.game_state = Pong.STATE_PLAYING

    def _draw_all(self):
        self.window.fill(self.bg_color)
        self.paddle_1.draw()
        self.paddle_2.draw()
        match self.game_state:
            case Pong.STATE_PLAYING:
                self.ball.draw()
                self.scoreboard.draw_division()
            case Pong.STATE_PAUSE:
                self.ball.draw()
                self.scoreboard.draw_text("GAME PAUSED")
            case Pong.STATE_COUNTDOWN:
                self.timer.draw()
            case Pong.STATE_START:
                self.scoreboard.draw_text("WELCOME TO PONG")
                self.scoreboard.draw_text(
                    "press ENTER to play",
                    self.scoreboard.font_size,
                    int(self.scoreboard.font_size / 2),
                )
            case Pong.STATE_GAME_OVER:
                if self.scoreboard.p1_score == self.settings.target_score:
                    self.scoreboard.draw_text("YOU WIN! CONGRATULATIONS!")
                else:
                    self.scoreboard.draw_text("YOU LOSE! DON'T GIVE UP!")
                self.scoreboard.draw_text(
                    "press ENTER to play again or ESC to quit",
                    self.scoreboard.font_size,
                    int(self.scoreboard.font_size / 2),
                )

        if self.game_state != Pong.STATE_START:
            self.scoreboard.draw_score()

    def _is_game_over(self):
        if (
            self.scoreboard.p1_score == self.settings.target_score
            or self.scoreboard.p2_score == self.settings.target_score
        ):
            return True
        return False


if __name__ == "__main__":
    pong = Pong()
    pong.run()
