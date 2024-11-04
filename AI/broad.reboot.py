import pygame
import sys
import random

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước bảng và các biến
N = 15  # Kích thước ma trận (15x15)
WIN_CONDITION = 4  # Số ký tự liên tiếp để thắng
CELL_SIZE = 30  # Kích thước mỗi ô vuông
WIDTH, HEIGHT = N * CELL_SIZE, N * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LINE_WIDTH = 5

# Tạo màn hình và ma trận bảng cờ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cờ Caro 15x15 với AI")
board = [['' for _ in range(N)] for _ in range(N)]
current_player = "X"  # Người chơi bắt đầu

# Tải hình nền
background_image = pygame.image.load('./img/background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Kéo dài hình nền

# Vẽ lưới cờ
def draw_grid():
    # Vẽ hình nền trước
    screen.blit(background_image, (0, 0))  # Vẽ hình nền ở góc trên bên trái
    for i in range(1, N):
        pygame.draw.line(screen, BLACK, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), LINE_WIDTH)

# Vẽ ký hiệu X và O
def draw_symbols():
    for row in range(N):
        for col in range(N):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, row * CELL_SIZE + 10),
                                 (col * CELL_SIZE + CELL_SIZE - 10, row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
                pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE - 10, row * CELL_SIZE + 10),
                                 (col * CELL_SIZE + 10, row * CELL_SIZE + CELL_SIZE - 10), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 10, LINE_WIDTH)

# Kiểm tra chiến thắng
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

# Kiểm tra nếu bảng đầy
def is_full():
    return all(board[row][col] != '' for row in range(N) for col in range(N))

# Tìm nước đi tốt nhất của AI với chiến lược thông minh
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
            row, col = y // CELL_SIZE, x // CELL_SIZE
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
