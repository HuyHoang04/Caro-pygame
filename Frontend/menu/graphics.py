# graphics.py
import pygame
from constants import *

def draw_grid(screen):
    screen.fill(BACKGROUND_COLOR)  # Đặt màu nền cho màn hình

    # Vẽ khung bao quanh lưới
    pygame.draw.rect(screen, FRAME_COLOR, 
                     (GRID_OFFSET_X - FRAME_WIDTH, GRID_OFFSET_Y - FRAME_WIDTH, 
                      get_board_size() * CELL_SIZE + 2 * FRAME_WIDTH, get_board_size() * CELL_SIZE + 2 * FRAME_WIDTH))

    # Vẽ nền lưới
    pygame.draw.rect(screen, BLUE, 
                     (GRID_OFFSET_X, GRID_OFFSET_Y, get_board_size() * CELL_SIZE, get_board_size() * CELL_SIZE))

    # Vẽ các đường lưới
    for i in range(1, get_board_size()):
        pygame.draw.line(screen, BLACK, 
                         (GRID_OFFSET_X, GRID_OFFSET_Y + CELL_SIZE * i), 
                         (GRID_OFFSET_X + get_board_size() * CELL_SIZE, GRID_OFFSET_Y + CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, 
                         (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y), 
                         (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y + get_board_size() * CELL_SIZE), LINE_WIDTH)

def draw_symbols(screen, board):
    for row in range(get_board_size()):
        for col in range(get_board_size()):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (GRID_OFFSET_X + col * CELL_SIZE + 10, GRID_OFFSET_Y + row * CELL_SIZE + 10),
                                 (GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE - 10, GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
                pygame.draw.line(screen, RED, (GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE - 10, GRID_OFFSET_Y + row * CELL_SIZE + 10),
                                 (GRID_OFFSET_X + col * CELL_SIZE + 10, GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLACK, (GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2, 
                                                    GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 10, LINE_WIDTH)
