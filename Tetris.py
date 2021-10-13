import pygame
import random


class Tetris:
    height = 0
    width = 0
    field = []
    score = 0
    state = "START"
    Figure = None

    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = START
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()

    def new_figure(self):
        next_figure = Figure(3, 0)
        if self.intersects(next_figure):
            self.state = GAME_OVER
            return
        self.Figure = next_figure

    def go_down(self):
        self.Figure.y += 1
        if self.intersects():
            self.Figure.y -= 1
            self.freeze()

    def side(self, dx):
        old_x = self.Figure.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if (
                        j + self.Figure.x + dx > self.width - 1  # beyond right border
                        or j + self.Figure.x + dx < 0  # beyond left border
                    ):
                        edge = True
        if not edge:
            self.Figure.x += dx
        if self.intersects():
            self.Figure.x = old_x

    def left(self):
        self.side(-1)

    def right(self):
        self.side(1)

    def down(self):
        while not self.intersects():
            self.Figure.y += 1
        self.Figure.y -= 1
        self.freeze()

    def rotate(self):
        old_rotation = self.Figure.rotation
        self.Figure.rotate()
        if self.intersects():
            self.Figure.rotation = old_rotation

    def intersects(self, fig=None):
        fig = self.Figure if (fig is None) else fig
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in fig.image():
                    if (
                        i + fig.y > self.height - 1  # bottom intersection
                        # or i + fig.y < 0  #
                        or self.field[i + fig.y][j + fig.x] > 0  # figure intersection
                    ):
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    self.field[i + self.Figure.y][j + self.Figure.x] = (
                        self.Figure.type + 1
                    )
        self.break_lines()
        self.new_figure()

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
        self.score += lines ** 2

class Figure:
    x = 0
    y = 0

    """
    Figure-matrix:

    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15
    """

    Figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Gerade
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # Rev L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
        [[1, 2, 5, 6]],  # BLOCK
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Reverse S
    ]

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.Figures) - 1)
        self.color = brick_colors[self.type + 1]
        self.rotation = 0

    def image(self):
        return self.Figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.Figures[self.type])

primary_colors = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255,255),
    "GREY": (128, 128, 128)

}


brick_colors = [
    (0, 0, 0),
    (0, 240, 240),  # 4 in einer Reihe
    (0, 0, 240),    # Reverse L
    (240, 160, 0),  # L
    (240, 240, 0),   # Block
    (0, 240, 0),    # S
    (160, 0, 240),  # T
    (240, 0, 0),    # Reverse S

]

GAME_OVER = "game_over"
START = "start"

pygame.init()

screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Tetris")

done = False
fps = 2
clock = pygame.time.Clock()
counter = 0
zoom = 30

game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False

while not done:
    if game.state == START:
        game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and not game.state == GAME_OVER:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False

        if pressing_down:
            game.down()
        if pressing_left:
            game.left()
        if pressing_right:
            game.right()

    screen.fill(color=primary_colors["WHITE"])
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = primary_colors["GREY"]
                just_border = 1
            else:
                color = brick_colors[game.field[i][j]]
                just_border = 0
            pygame.draw.rect(
                screen,
                color,
                [30 + j * zoom, 30 + i * zoom, zoom, zoom],
                just_border,
            )

    if game.Figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.Figure.image():
                    pygame.draw.rect(
                        screen,
                        game.Figure.color,
                        [
                            30 + (j + game.Figure.x) * zoom,
                            30 + (i + game.Figure.y) * zoom,
                            zoom,
                            zoom,
                        ],
                    )

    gameover_font = pygame.font.SysFont("Calibri", 65, True, False)
    text_gameover = gameover_font.render("Game Over!\n Press Esc", True, (255, 215, 0))

    if game.state == GAME_OVER:
        screen.blit(text_gameover, [30, 250])

    score_font = pygame.font.SysFont("Calibri", 25, True, False)
    text_score = gameover_font.render("Score: " + str(game.score), True, (0, 0, 0))
    screen.blit(text_score, [0, 0])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()