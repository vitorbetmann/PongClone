class PongAi:
    def __init__(self, game):
        self.window = game.window_rect
        if game.player_paddle.name == "paddle 1":
            ai_paddle = game.paddle_2
        else:
            ai_paddle = game.paddle_1
        self.paddle = ai_paddle
        self.ball = game.ball

    def predict_move(self):
        match (self.ball.is_moving_right()):
            case True:
                if self.ball.centery > self.paddle.centery:
                    self.paddle.move_down()
                elif self.ball.centery < self.paddle.centery:
                    self.paddle.move_up()
            case False:
                if self.paddle.centery < self.ball.centery:
                    self.paddle.slowly_move_down()
                elif self.paddle.centery > self.ball.centery:
                    self.paddle.slowly_move_up()
