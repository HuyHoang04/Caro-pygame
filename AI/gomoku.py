# gomoku.py

import pygame

# Kích thước cấu hình
SCREEN_SIZE = 600
BOARD_SIZE = 15
CELL_SIZE = SCREEN_SIZE // BOARD_SIZE

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Gomoku:
    def __init__(self):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_turn = "X"

    def draw_board(self, screen):
        # Vẽ lưới bàn cờ
        for i in range(BOARD_SIZE):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE))
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE))

    def draw_piece(self, screen, x, y, piece):
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        if piece == "X":
            offset = CELL_SIZE // 3
            pygame.draw.line(screen, RED, (center[0] - offset, center[1] - offset), 
                             (center[0] + offset, center[1] + offset), 2)
            pygame.draw.line(screen, RED, (center[0] + offset, center[1] - offset), 
                             (center[0] - offset, center[1] + offset), 2)
        elif piece == "O":
            pygame.draw.circle(screen, BLACK, center, CELL_SIZE // 3, 2)

    def draw_pieces(self, screen):
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece:
                    self.draw_piece(screen, x, y, piece)

    def reset_game(self):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_turn = "X"
    
    def switch_turn(self):
        self.current_turn = "O" if self.current_turn == "X" else "X"
