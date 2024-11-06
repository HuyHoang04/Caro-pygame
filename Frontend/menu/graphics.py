# graphics.py
import pygame
from constants import *

def draw_grid(screen):
    screen.blit(BACKGROUND_COLOR, (0, 0))  # Đặt màu nền cho màn hình

    # Vẽ khung bao quanh lưới
    pygame.draw.rect(screen, FRAME_COLOR, 
                     (GRID_OFFSET_X - FRAME_WIDTH, GRID_OFFSET_Y - FRAME_WIDTH, 
                      get_board_size() * CELL_SIZE + 2 * FRAME_WIDTH, get_board_size() * CELL_SIZE + 2 * FRAME_WIDTH))

    # Vẽ nền lưới
    pygame.draw.rect(screen, BLACK, 
                     (GRID_OFFSET_X, GRID_OFFSET_Y, get_board_size() * CELL_SIZE, get_board_size() * CELL_SIZE))

    # Vẽ các đường lưới
    for i in range(1, get_board_size()):
        pygame.draw.line(screen, WHITE, 
                         (GRID_OFFSET_X, GRID_OFFSET_Y + CELL_SIZE * i), 
                         (GRID_OFFSET_X + get_board_size() * CELL_SIZE, GRID_OFFSET_Y + CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, 
                         (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y), 
                         (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y + get_board_size() * CELL_SIZE), LINE_WIDTH)

def draw_symbols(screen, board):
    for row in range(get_board_size()):
        for col in range(get_board_size()):
            if board[row][col] == "X":
                # Vẽ iconX vào vị trí tương ứng
                screen.blit(ICON_X, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))
            elif board[row][col] == "O":
                # Vẽ iconO vào vị trí tương ứng
                screen.blit(ICON_O, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))

def draw_winning_line(screen, positions):
    if not positions:
        return

    # Lấy tọa độ của ô đầu và ô cuối trong chuỗi thắng
    start_pos = positions[0]
    end_pos = positions[-1]

    # Tính tọa độ điểm đầu và điểm cuối cho đường thắng
    start_x = GRID_OFFSET_X + start_pos[1] * CELL_SIZE + CELL_SIZE // 2
    start_y = GRID_OFFSET_Y + start_pos[0] * CELL_SIZE + CELL_SIZE // 2
    end_x = GRID_OFFSET_X + end_pos[1] * CELL_SIZE + CELL_SIZE // 2
    end_y = GRID_OFFSET_Y + end_pos[0] * CELL_SIZE + CELL_SIZE // 2

    # Vẽ đường thắng
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), LINE_WIDTH * 2)