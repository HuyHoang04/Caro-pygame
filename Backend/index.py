import pygame
import sys
import random
import time

# Khởi tạo pygame và cài đặt các thông số cơ bản
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caro Game")

# Các thông số
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRID_SIZE = 20
CELL_SIZE = 30
TIME_LIMIT = 30  # giới hạn thời gian 30 giây

# Bảng điểm và lịch sử chơi
history = []
font = pygame.font.SysFont(None, 30)

# Hàm hiển thị thông báo
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Kiểm tra thắng thua
def check_win(board, symbol):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == symbol:
                # Kiểm tra hàng ngang
                if x + 4 < GRID_SIZE and all(board[y][x + i] == symbol for i in range(5)):
                    return True
                # Kiểm tra hàng dọc
                if y + 4 < GRID_SIZE and all(board[y + i][x] == symbol for i in range(5)):
                    return True
                # Kiểm tra đường chéo /
                if x + 4 < GRID_SIZE and y + 4 < GRID_SIZE and all(board[y + i][x + i] == symbol for i in range(5)):
                    return True
                # Kiểm tra đường chéo \
                if x - 4 >= 0 and y + 4 < GRID_SIZE and all(board[y + i][x - i] == symbol for i in range(5)):
                    return True
    return False

# AI di chuyển
def ai_move(board):
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if board[y][x] == "":
            board[y][x] = "O"
            break

# Hàm khởi tạo trò chơi
def game():
    # Khởi tạo trạng thái
    board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_turn = True
    start_time = time.time()

    # Vòng lặp trò chơi
    running = True
    while running:
        screen.fill(WHITE)

        # Kiểm tra thời gian
        elapsed_time = time.time() - start_time
        remaining_time = TIME_LIMIT - int(elapsed_time)
        if remaining_time <= 0:
            player_turn = False
            ai_move(board)
            start_time = time.time()
            player_turn = True

        # Vẽ bàn cờ
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if board[y][x] == "X":
                    pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 3)
                    pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 3)
                elif board[y][x] == "O":
                    pygame.draw.circle(screen, BLUE, rect.center, CELL_SIZE // 3, 3)

        # Hiển thị thời gian
        draw_text(f"Thời gian còn lại: {remaining_time}s", font, BLACK, screen, SCREEN_WIDTH - 150, 30)

        # Kiểm tra sự kiện người dùng
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if board[grid_y][grid_x] == "":
                    board[grid_y][grid_x] = "X"
                    if check_win(board, "X"):
                        history.append(("Player", "Win"))
                        running = False
                    else:
                        player_turn = False
                        ai_move(board)
                        if check_win(board, "O"):
                            history.append(("Player", "Lose"))
                            running = False
                    start_time = time.time()
                    player_turn = True

        # Cập nhật màn hình
        pygame.display.flip()

# Chạy trò chơi
game()
