import pygame

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
N = 15  # Kích thước ma trận (15x15)
WIN_CONDITION = 5  # Số ký tự liên tiếp để thắng
CELL_SIZE = 30  # Kích thước mỗi ô vuông
WIDTH = 1100
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (173, 216, 230)  # Màu nền lưới
BACKGROUND_COLOR = (240, 248, 255)  # Màu nền màn hình
LINE_WIDTH = 5
FRAME_COLOR = (0, 128, 128)  # Màu khung bao quanh lưới
FRAME_WIDTH = 10  # Độ dày của khung

# Thiết lập vị trí lưới để nằm giữa màn hình
GRID_OFFSET_X = (WIDTH - (N * CELL_SIZE)) // 2
GRID_OFFSET_Y = (HEIGHT - (N * CELL_SIZE)) // 2
