import pygame

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
N = 18  # Kích thước ma trận ban đầu
WIN_CONDITION = 5  # Số ký tự liên tiếp để thắng
CELL_SIZE = 35  # Kích thước mỗi ô vuông
WIDTH = 1300
HEIGHT = 650
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
    update_grid_offset()

def get_board_size():
    return N

update_grid_offset()
