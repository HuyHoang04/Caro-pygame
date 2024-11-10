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
    total_width = get_board_size() * CELL_SIZE
    total_height = get_board_size() * CELL_SIZE
    
    # Căn giữa bàn cờ trong màn hình (hoặc đặt nó ở góc trái nếu quá rộng)
    GRID_OFFSET_X = (WIDTH - total_width) // 2
    GRID_OFFSET_Y = (HEIGHT - total_height) // 2
    
    # Kiểm tra lại các giá trị GRID_OFFSET_X và GRID_OFFSET_Y
    print(f"GRID_OFFSET_X: {GRID_OFFSET_X}, GRID_OFFSET_Y: {GRID_OFFSET_Y}")

# Hàm thay đổi kích thước bàn cờ và tự động căn giữa
def set_board_size(board_size):
    global N, CELL_SIZE
    N = board_size  # Cập nhật lại kích thước bàn cờ
    
    # Cập nhật CELL_SIZE theo kích thước bàn cờ (có thể thay đổi theo yêu cầu)
    if N > 15:
        CELL_SIZE = 40
    elif N > 10:
        CELL_SIZE = 50
    else:
        CELL_SIZE = 60
    
    # Gọi hàm cập nhật lại GRID_OFFSET_X, GRID_OFFSET_Y
    update_grid_offset()

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
