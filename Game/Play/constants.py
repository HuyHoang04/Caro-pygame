import pygame, random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
board_sizes = ["8x8", "10x10", "15x15", "18x18", "20x20"]  # Các kích thước bảng
current_size_index = 0  
N = int(board_sizes[current_size_index].split('x')[0])  # Kích thước ma trận ban đầu
WIN_CONDITION = 5  # Số ký tự liên tiếp để thắng
CELL_SIZE = 35  # Kích thước mỗi ô vuông
WIDTH = 1280  # Đảm bảo kích thước này trùng với SCREEN trong menu.py
HEIGHT = 850  # Đảm bảo kích thước này trùng với SCREEN trong menu.py
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Màu nền lưới
BACKGROUND_COLOR = pygame.image.load("assets/Background3.jpg")  # Màu nền màn hình
LINE_WIDTH = 2
FRAME_COLOR = (0, 128, 128)  # Màu khung bao quanh lưới
FRAME_WIDTH = 6  # Độ dày của khung

# Tải các biểu tượng X và O
ICON_X = pygame.image.load("assets/iconX.png")  # Đường dẫn tới ảnh iconX.png
ICON_O = pygame.image.load("assets/iconO.png")  # Đường dẫn tới ảnh iconO.png

# Cân nhắc thay đổi kích thước icon để phù hợp với CELL_SIZE (nếu cần thiết)
ICON_X = pygame.transform.scale(ICON_X, (CELL_SIZE - 10, CELL_SIZE - 10))
ICON_O = pygame.transform.scale(ICON_O, (CELL_SIZE - 10, CELL_SIZE - 10))


# Thiết lập vị trí lưới để nằm giữa màn hình
def update_grid_offset():
    global GRID_OFFSET_X, GRID_OFFSET_Y
    
    # Tính toán tổng chiều rộng và chiều cao của bàn cờ
    total_width = N * CELL_SIZE
    total_height = N * CELL_SIZE
    
    # Căn giữa bàn cờ trong màn hình (hoặc đặt nó ở góc trái nếu quá rộng)
    GRID_OFFSET_X = (WIDTH - total_width) // 2
    GRID_OFFSET_Y = (HEIGHT - total_height) // 2

def get_board_position(mouse_pos):
    x, y = mouse_pos
    if GRID_OFFSET_X <= x < GRID_OFFSET_X + N * CELL_SIZE and GRID_OFFSET_Y <= y < GRID_OFFSET_Y + N * CELL_SIZE:
        row = (y - GRID_OFFSET_Y) // CELL_SIZE
        col = (x - GRID_OFFSET_X) // CELL_SIZE
        return row, col
    return None, None

def get_random_empty_cell(board):
    empty_cells = [(r, c) for r in range(N) for c in range(N) if board[r][c] == ""]
    if empty_cells:
        return random.choice(empty_cells)
    return None, None

# Gọi cập nhật lần đầu tiên
update_grid_offset()

import pygame
from constants import *

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Vẽ lưới bàn cờ và khung bàn cờ
def draw_grid(screen):
    """
    Vẽ lưới bàn cờ vào màn hình.
    """
    screen.blit(BACKGROUND_COLOR, (0, 0))  # Đặt màu nền cho màn hình


    pygame.draw.rect(screen, FRAME_COLOR, 
                     (GRID_OFFSET_X - FRAME_WIDTH, GRID_OFFSET_Y - FRAME_WIDTH, 
                      N * CELL_SIZE + 2 * FRAME_WIDTH, N * CELL_SIZE + 2 * FRAME_WIDTH))


    pygame.draw.rect(screen, BLACK, 
                     (GRID_OFFSET_X, GRID_OFFSET_Y, N * CELL_SIZE, N * CELL_SIZE))


    for i in range(1, N):
        pygame.draw.line(screen, WHITE, 
                         (GRID_OFFSET_X, GRID_OFFSET_Y + CELL_SIZE * i), 
                         (GRID_OFFSET_X + N * CELL_SIZE, GRID_OFFSET_Y + CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, 
                         (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y), 
                         (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y + N * CELL_SIZE), LINE_WIDTH)


def draw_symbols(screen, board):
    """
    Vẽ các ký hiệu "X" và "O" vào bàn cờ.
    """
    for row in range(N):
        for col in range(N):
            if board[row][col] == "X":
                screen.blit(ICON_X, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))
            elif board[row][col] == "O":
                screen.blit(ICON_O, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))


def draw_winning_line(screen, positions):
    """
    Vẽ đường thắng nếu có người chiến thắng.
    """
    if not positions:
        return

    start_pos = positions[0]
    end_pos = positions[-1]

    start_x = GRID_OFFSET_X + start_pos[1] * CELL_SIZE + CELL_SIZE // 2
    start_y = GRID_OFFSET_Y + start_pos[0] * CELL_SIZE + CELL_SIZE // 2
    end_x = GRID_OFFSET_X + end_pos[1] * CELL_SIZE + CELL_SIZE // 2
    end_y = GRID_OFFSET_Y + end_pos[0] * CELL_SIZE + CELL_SIZE // 2

    # Vẽ đường thắng
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), LINE_WIDTH * 2)

