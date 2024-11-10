import pygame
from constants import *

def set_board_size(board_size):
    """
    Hàm này dùng để tính toán lại kích thước bàn cờ và căn giữa nó trên màn hình.
    """
    global GRID_OFFSET_X, GRID_OFFSET_Y, CELL_SIZE
    
    # Tính toán lại offset và các thông số liên quan khi thay đổi kích thước bàn cờ
    GRID_SIZE = board_size  # Kích thước bàn cờ (số lượng ô trên một chiều)
    
    # Cập nhật lại CELL_SIZE nếu cần (ví dụ muốn thay đổi kích thước ô)
    if GRID_SIZE > 15:
        CELL_SIZE = 40
    elif GRID_SIZE > 10:
        CELL_SIZE = 50
    else:
        CELL_SIZE = 60

    # Tính toán lại vị trí căn giữa bàn cờ
    GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
    GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_SIZE * CELL_SIZE) // 2


def draw_grid(screen):
    """
    Vẽ lưới bàn cờ vào màn hình.
    """
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
    """
    Vẽ các ký hiệu "X" và "O" vào bàn cờ.
    """
    for row in range(get_board_size()):
        for col in range(get_board_size()):
            if board[row][col] == "X":
                # Vẽ icon X vào vị trí tương ứng
                screen.blit(ICON_X, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))
            elif board[row][col] == "O":
                # Vẽ icon O vào vị trí tương ứng
                screen.blit(ICON_O, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))


def draw_winning_line(screen, positions):
    """
    Vẽ đường thắng nếu có người chiến thắng.
    """
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
