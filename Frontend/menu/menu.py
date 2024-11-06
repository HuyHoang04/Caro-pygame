# menu.py
import pygame, sys, random
from button import Button
from constants import *
from graphics import draw_grid, draw_symbols
from checkwin import check_winner

# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình hiển thị
SCREEN = pygame.display.set_mode((1280, 850))
pygame.display.set_caption("Menu")

# Tải ảnh nền
BG = pygame.image.load("assets/Background2.jpg")

# Hàm lấy font chữ
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Thiết lập các mức độ khó và kích thước bảng
levels = ["EASY", "MEDIUM", "HARD"]
current_level_index = 0

board_sizes = ["8x8", "10x10", "15x15", "18x18"]
current_size_index = 2  # Mặc định là 15x15

# Hàm chính để chơi game
def play():
    # Cập nhật kích thước bàn cờ và vị trí lưới sau khi thay đổi kích thước
    board_size = int(board_sizes[current_size_index].split('x')[0])
    set_board_size(board_size)
    update_grid_offset()  # Cập nhật vị trí lưới để căn giữa màn hình

    # Khởi tạo bàn cờ trống
    board = [["" for _ in range(get_board_size())] for _ in range(get_board_size())]
    player_turn = True  # Đánh dấu lượt của người chơi

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        
        # Vẽ lưới và ký hiệu với lưới đã được căn giữa
        draw_grid(SCREEN)
        draw_symbols(SCREEN, board)

        PLAY_BACK = Button(image=None, pos=(660, 785), 
                           text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nút BACK
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

                if player_turn:  # Chỉ cho phép đánh dấu nếu là lượt của người chơi
                    col = (PLAY_MOUSE_POS[0] - GRID_OFFSET_X) // CELL_SIZE
                    row = (PLAY_MOUSE_POS[1] - GRID_OFFSET_Y) // CELL_SIZE
                    if 0 <= row < board_size and 0 <= col < board_size and board[row][col] == "":
                        board[row][col] = "X"  # Đánh dấu của người chơi
                        if check_winner(board, "X"):
                            print("Player wins!")
                            pygame.time.wait(2000)
                            main_menu()  # Quay lại menu chính nếu người chơi thắng
                        player_turn = False  # Chuyển sang lượt của máy

        if not player_turn:  # Lượt của máy
            # Đặt thuật toán AI đơn giản ở đây (ví dụ chỉ chọn ô trống đầu tiên tìm thấy)
            for row in range(board_size):
                for col in range(board_size):
                    if board[row][col] == "":
                        board[row][col] = "O"  # Máy đánh dấu
                        if check_winner(board, "O"):
                            print("AI wins!")
                            pygame.time.wait(2000)
                            main_menu()  # Quay lại menu chính nếu máy thắng
                        player_turn = True  # Chuyển lại lượt cho người chơi
                        break
                if player_turn:
                    break

        pygame.display.update()

# Hàm menu chính
def main_menu():
    global current_level_index, current_size_index

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CARO GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 480), 
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        LEFT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 250), 
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 250), 
                                   text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        LEVEL_TEXT = get_font(35).render(levels[current_level_index], True, "#d7fcd4")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 250))

        LEFT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 350), 
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 350), 
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        SIZE_TEXT = get_font(35).render(board_sizes[current_size_index], True, "#d7fcd4")
        SIZE_RECT = SIZE_TEXT.get_rect(center=(640, 350))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
        SCREEN.blit(SIZE_TEXT, SIZE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, LEFT_ARROW_LEVEL, RIGHT_ARROW_LEVEL, LEFT_ARROW_SIZE, RIGHT_ARROW_SIZE]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if LEFT_ARROW_LEVEL.checkForInput(MENU_MOUSE_POS):
                    current_level_index = (current_level_index - 1) % len(levels)
                if RIGHT_ARROW_LEVEL.checkForInput(MENU_MOUSE_POS):
                    current_level_index = (current_level_index + 1) % len(levels)
                if LEFT_ARROW_SIZE.checkForInput(MENU_MOUSE_POS):
                    current_size_index = (current_size_index - 1) % len(board_sizes)
                    set_board_size(int(board_sizes[current_size_index].split('x')[0]))
                    update_grid_offset()
                if RIGHT_ARROW_SIZE.checkForInput(MENU_MOUSE_POS):
                    current_size_index = (current_size_index + 1) % len(board_sizes)
                    set_board_size(int(board_sizes[current_size_index].split('x')[0]))
                    update_grid_offset()

        pygame.display.update()

main_menu()
