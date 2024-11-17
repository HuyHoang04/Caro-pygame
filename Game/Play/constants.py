import pygame, random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
board_sizes = ["8x8", "10x10", "15x15", "18x18"]  # Các kích thước bảng
current_size_index = 3  # Kích thước mặc định (8x8)
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
