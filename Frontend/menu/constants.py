# constants.py
import pygame, random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
N = 18  # Kích thước ma trận ban đầu
WIN_CONDITION = 5  # Số ký tự liên tiếp để thắng
CELL_SIZE = 35  # Kích thước mỗi ô vuông
WIDTH = 1280  # Đảm bảo kích thước này trùng với SCREEN trong menu.py
HEIGHT = 850  # Đảm bảo kích thước này trùng với SCREEN trong menu.py
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (173, 216, 230)  # Màu nền lưới
BACKGROUND_COLOR = (240, 248, 255)  # Màu nền màn hình
LINE_WIDTH = 2
FRAME_COLOR = (0, 128, 128)  # Màu khung bao quanh lưới
FRAME_WIDTH = 6  # Độ dày của khung

# Thiết lập vị trí lưới để nằm giữa màn hình
def update_grid_offset():
    global GRID_OFFSET_X, GRID_OFFSET_Y
    GRID_OFFSET_X = (WIDTH - (N * CELL_SIZE)) // 2
    GRID_OFFSET_Y = (HEIGHT - (N * CELL_SIZE)) // 2

def set_board_size(size):
    global N
    N = size
    update_grid_offset()  # Cập nhật vị trí mỗi khi thay đổi kích thước bàn cờ

def get_board_size():
    return N


def get_board_position(mouse_pos):
    x, y = mouse_pos
    if GRID_OFFSET_X <= x < GRID_OFFSET_X + get_board_size() * CELL_SIZE and GRID_OFFSET_Y <= y < GRID_OFFSET_Y + get_board_size() * CELL_SIZE:
        row = (y - GRID_OFFSET_Y) // CELL_SIZE
        col = (x - GRID_OFFSET_X) // CELL_SIZE
        return row, col
    return None, None

def get_random_empty_cell(board):
    empty_cells = [(r, c) for r in range(get_board_size()) for c in range(get_board_size()) if board[r][c] == ""]
    if empty_cells:
        return random.choice(empty_cells)
    return None, None

# Gọi cập nhật lần đầu tiên
update_grid_offset()
