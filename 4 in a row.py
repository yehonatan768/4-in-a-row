import numpy as np
import pygame
import sys
import math
import pandas

class PygameSetup:
    def __init__(self, p_X, p_Y):
        pygame.init()
        pygame.display.set_caption('Four In A Row')
        self.screen = pygame.display.set_mode((p_X, p_Y))
        self.clock = pygame.time.Clock()
        self.font = None

    def getScreen(self):
        return self.screen

    def update(self):
        pygame.display.flip()
        self.clock.tick(100)

    def blit(self, pic, x):
        self.screen.blit(pic, x)

    def fill(self, color):
        self.screen.fill(color)

    def draw_text(self, text, color, size, x, y):
        font1 = pygame.font.Font(self.font, size)
        surface = font1.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def close(self):
        self.close()


# global Const Parameters
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
SCALE = 80
# define width and height of board
width = COLUMN_COUNT * SCALE
height = (ROW_COUNT + 1) * SCALE
screen = PygameSetup(height, width)
RADIUS = int(SCALE / 2 - 5)

GAME_OVER = False
TURN = 0


class Game:
    def __init__(self):
        self.board = self.create_board()
        print(self.board)

    @staticmethod
    def create_board():
        return np.zeros((ROW_COUNT, COLUMN_COUNT))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print("\n\n\n")
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and \
                        self.board[r][
                            c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and \
                        self.board[r + 3][
                            c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][
                    c + 2] == piece and \
                        self.board[r + 3][
                            c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][
                    c + 2] == piece and \
                        self.board[r - 3][
                            c + 3] == piece:
                    return True

    def draw_board(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen.getScreen(), BLUE,
                                 (c * SCALE, r * SCALE + SCALE, SCALE, SCALE))
                pygame.draw.circle(screen.getScreen(), BLACK, (
                    int(c * SCALE + SCALE / 2), int(r * SCALE + SCALE + SCALE / 2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen.getScreen(), RED, (
                        int(c * SCALE + SCALE / 2), height - int(r * SCALE + SCALE / 2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen.getScreen(), YELLOW, (
                        int(c * SCALE + SCALE / 2), height - int(r * SCALE + SCALE / 2)), RADIUS)
        pygame.display.update()

    def turn(self, x, player_id, color):
        global GAME_OVER
        col = int(math.floor(x / SCALE))
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, player_id)

            if self.winning_move(player_id):
                screen.draw_text("Player " + str(player_id) + " wins!!", color, int(80 * SCALE / 100),
                                 int(150 * SCALE / 100), int(30 * SCALE / 100))
                GAME_OVER = True

    def event_handler(self, x, event, click):
        global GAME_OVER, TURN
        if TURN == 0:
            color = RED
        else:
            color = YELLOW
        if event.type == pygame.MOUSEMOTION:

            pygame.draw.rect(screen.getScreen(), BLACK, (0, 0, width, SCALE))

            if TURN == 0:
                pygame.draw.circle(screen.getScreen(), RED, (x, int(SCALE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen.getScreen(), YELLOW, (x, int(SCALE / 2)), RADIUS)

        if event.type == pygame.MOUSEBUTTONDOWN and click[0] == 1:
            pygame.draw.rect(screen.getScreen(), BLACK, (0, 0, width, SCALE))
            # print(event.pos)
            self.turn(x, TURN + 1, color)

            TURN += 1
            TURN = TURN % 2
            self.print_board()

    def play(self):
        self.draw_board()

        while not GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                click = pygame.mouse.get_pressed()
                x, _ = pygame.mouse.get_pos()
                self.event_handler(x, event, click)

            self.draw_board()
            if GAME_OVER:
                pygame.time.wait(3000)
            screen.update()


game = Game()
game.play()
