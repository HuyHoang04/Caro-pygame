import pygame
import sys
import random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
N = 15  # Kích thước ma trận (15x15)
WIN_CONDITION = 4  # Số ký tự liên tiếp để thắng
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

# Tạo màn hình và ma trận bảng cờ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Caro 15x15 với AI")
board = [['' for _ in range(N)] for _ in range(N)]
current_player = "X"  # Người chơi bắt đầu

# Thiết lập vị trí lưới để nằm giữa màn hình
grid_offset_x = (WIDTH - (N * CELL_SIZE)) // 2
grid_offset_y = (HEIGHT - (N * CELL_SIZE)) // 2

# Vẽ lưới cờ với khung và nền
def draw_grid():
    screen.fill(BACKGROUND_COLOR)  # Đặt màu nền cho màn hình

    # Vẽ khung bao quanh lưới
    pygame.draw.rect(screen, FRAME_COLOR, 
                     (grid_offset_x - FRAME_WIDTH, grid_offset_y - FRAME_WIDTH, 
                      N * CELL_SIZE + 2 * FRAME_WIDTH, N * CELL_SIZE + 2 * FRAME_WIDTH))

    # Vẽ nền lưới
    pygame.draw.rect(screen, BLUE, 
                     (grid_offset_x, grid_offset_y, N * CELL_SIZE, N * CELL_SIZE))

    # Vẽ các đường lưới
    for i in range(1, N):
        pygame.draw.line(screen, BLACK, 
                         (grid_offset_x, grid_offset_y + CELL_SIZE * i), 
                         (grid_offset_x + N * CELL_SIZE, grid_offset_y + CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, 
                         (grid_offset_x + CELL_SIZE * i, grid_offset_y), 
                         (grid_offset_x + CELL_SIZE * i, grid_offset_y + N * CELL_SIZE), LINE_WIDTH)

# Vẽ ký hiệu X và O
def draw_symbols():
    for row in range(N):
        for col in range(N):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (grid_offset_x + col * CELL_SIZE + 10, grid_offset_y + row * CELL_SIZE + 10),
                                 (grid_offset_x + col * CELL_SIZE + CELL_SIZE - 10, grid_offset_y + row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
                pygame.draw.line(screen, RED, (grid_offset_x + col * CELL_SIZE + CELL_SIZE - 10, grid_offset_y + row * CELL_SIZE + 10),
                                 (grid_offset_x + col * CELL_SIZE + 10, grid_offset_y + row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLACK, (grid_offset_x + col * CELL_SIZE + CELL_SIZE // 2, 
                                                    grid_offset_y + row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 10, LINE_WIDTH)
def check_winner():
    for row in range(N):
        for col in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row][col + i] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    for col in range(N):
        for row in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row + i][col] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    for row in range(N - WIN_CONDITION + 1):
        for col in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row + i][col + i] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    for row in range(WIN_CONDITION - 1, N):
        for col in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row - i][col + i] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    return None


def is_full():
    return all(board[row][col] != '' for row in range(N) for col in range(N))
def smart_move():
    # Kiểm tra xem máy có thể thắng ngay không
    for row in range(N):
        for col in range(N):
            if board[row][col] == '':
                board[row][col] = "O"
                if check_winner() == "O":
                    return  # Máy thắng
                board[row][col] = ''  # Hoàn tác

    # Kiểm tra xem người chơi có thể thắng ở nước đi tiếp theo không
    for row in range(N):
        for col in range(N):
            if board[row][col] == '':
                board[row][col] = "X"
                if check_winner() == "X":
                    board[row][col] = "O"  # Chặn người chơi
                    return
                board[row][col] = ''  # Hoàn tác

    # Nếu không có nước đi thắng hay chặn, chọn một nước đi ngẫu nhiên
    while True:
        row = random.randint(0, N-1)
        col = random.randint(0, N-1)
        if board[row][col] == '':
            board[row][col] = "O"
            return

# Xử lý khi người chơi click vào ô
def player_move(row, col):
    global current_player
    if board[row][col] == '' and not check_winner():
        board[row][col] = current_player
        if check_winner() or is_full():
            return
        current_player = "O" if current_player == "X" else "X"
        if current_player == "O":
            smart_move()  # Máy đánh theo chiến lược thông minh
            current_player = "X"

# Vòng lặp trò chơi
draw_grid()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and current_player == "X":
            x, y = event.pos
            row, col = (y - grid_offset_y) // CELL_SIZE, (x - grid_offset_x) // CELL_SIZE
            if 0 <= row < N and 0 <= col < N:  # Ensure valid click
                player_move(row, col)
                draw_symbols()
                winner = check_winner()
                if winner:
                    print(f"{winner} thắng!")
                    pygame.time.wait(2000)
                    board = [['' for _ in range(N)] for _ in range(N)]
                    draw_grid()
                    draw_symbols()

    draw_symbols()
    pygame.display.update()
