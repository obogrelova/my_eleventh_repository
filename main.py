import pygame
import random

pygame.init()

WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тетрис")

COLORS = [
    (0, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128),
    (255, 255, 0)
]

SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[1, 2, 5, 6]],
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
    [[1, 2, 4, 5], [0, 4, 5, 9]],
    [[0, 1, 5, 6], [2, 4, 5, 7]],
    [[1, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 9], [1, 5, 8, 9]],
    [[0, 1, 2, 5], [1, 4, 5, 9], [0, 1, 2, 5], [1, 5, 6, 9]]
]

class Figure:
    def __init__(self, shape, color):
        self.x, self.y = COLS // 2, 0
        self.shape = shape
        self.color = color
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


class Tetris:
    def __init__(self):
        self.board = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.game_over = False
        self.current_figure = self.new_figure()

    def new_figure(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return Figure(shape, color)

    def intersects(self):
        for i in range(4):
            x = (self.current_figure.x + self.current_figure.image()[i] % 4) % COLS
            y = (self.current_figure.y + self.current_figure.image()[i] // 4)
            if y >= ROWS or x >= COLS or x < 0 or self.board[y][x] != (0, 0, 0):
                return True
        return False

    def freeze(self):
        for i in range(4):
            x = (self.current_figure.x + self.current_figure.image()[i] % 4) % COLS
            y = (self.current_figure.y + self.current_figure.image()[i] // 4)
            self.board[y][x] = self.current_figure.color
        self.clear_lines()
        self.current_figure = self.new_figure()
        if self.intersects():
            self.game_over = True

    def clear_lines(self):
        lines = 0
        for y in range(ROWS - 1, -1, -1):
            if all(self.board[y][x] != (0, 0, 0) for x in range(COLS)):
                del self.board[y]
                self.board.insert(0, [(0, 0, 0) for _ in range(COLS)])
                lines += 1
        self.score += lines ** 2

    def move(self, dx, dy):
        self.current_figure.x += dx
        self.current_figure.y += dy
        if self.intersects():
            self.current_figure.x -= dx
            self.current_figure.y -= dy
            if dy != 0:
                self.freeze()

    def rotate(self):
        old_rotation = self.current_figure.rotation
        self.current_figure.rotate()
        if self.intersects():
            self.current_figure.rotation = old_rotation

    def draw(self):
        SCREEN.fill((0, 0, 0))
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x] != (0, 0, 0):
                    pygame.draw.rect(SCREEN, self.board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for i in range(4):
            x = (self.current_figure.x + self.current_figure.image()[i] % 4) % COLS
            y = (self.current_figure.y + self.current_figure.image()[i] // 4)
            pygame.draw.rect(SCREEN, self.current_figure.color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0

    running = True
    while running:
        dx = 0
        fall_speed = 500
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > fall_speed:
            fall_time = 0
            game.move(0, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()

        game.move(dx, 0)
        game.draw()

        if game.game_over:
            running = False

    pygame.quit()

if __name__=="__main__":
    main()