class Settings:
    def __init__(self):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        self.PADDLE_WIDTH = 20
        self.PADDLE_HEIGHT = 100
        self.PADDLE_OFFSET = 3
        self.PADDLE_SPEED = 8
        self.BALL_X_SPEED = 10
        self.BALL_Y_SPEED = 9

        self.BALL_SIDE_LENGTH = 15

        self.SCOREBOARD_FONT_SIZE = 70

        self.FPS = 60

        self.bg_color = "black"
        self.scoreboard_color = self.paddle_color = self.ball_color = "white"
        self.target_score = 3
