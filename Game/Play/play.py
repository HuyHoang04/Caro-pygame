# menu.py
import pygame, sys, random, pyperclip
from button import Button
from constants import *

from checkwin import check_winner
from leaderboard import save_score, load_leaderboard


# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình hiển thị
SCREEN = pygame.display.set_mode((1280, 850))
pygame.display.set_caption("Menu")

# Tải ảnh nền
BG = pygame.image.load("assets/Background3.jpg")
player_name = ""

# Hàm lấy font chữ
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Hàm để tạo ô nhập liệu và căn giữa văn bản, vẽ con trỏ nhấp nháy
def draw_input_box(SCREEN, x, y, width, height, text, font, base_color, active_color, cursor_visible):
    # Tạo một ô input box
    input_box = pygame.Rect(x, y, width, height)
    pygame.draw.rect(SCREEN, base_color, input_box)  # Vẽ ô input box

    # Tạo surface từ văn bản
    text_surface = font.render(text, True, (0, 0, 0))  # Văn bản màu đen
    text_rect = text_surface.get_rect(center=input_box.center)  # Căn giữa văn bản

    # Vẽ văn bản vào ô
    SCREEN.blit(text_surface, text_rect)

    # Vẽ con trỏ nhấp nháy
    if cursor_visible:
        cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
        pygame.draw.rect(SCREEN, (0, 0, 0), cursor_rect)  # Vẽ con trỏ nhấp nháy (màu đen)

    return input_box


# Thiết lập các mức độ khó và kích thước bảng
levels = ["EASY", "MEDIUM", "HARD"]
current_level_index = 0

mode = ["PLAYER", "COMPUTER"]
current_mode_index = 1

# Hàm chính để chơi game
def play():
    global player_name
    board_size = int(board_sizes[current_size_index].split('x')[0])

    # Khởi tạo bàn cờ
    board = [["" for _ in range(N)] for _ in range(N)]
    history = []  # Lưu tất cả các nước đi của X và O
    turn = 0  # 0 là lượt của X (người chơi), 1 là lượt của O (người chơi)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")

        draw_grid(SCREEN)
        draw_symbols(SCREEN, board)

        PLAY_BACK = Button(image=None, pos=(660, 795), text_input="BACK", font=get_font(45), base_color="White", hovering_color="Red")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        UNDO_BUTTON = Button(image=None, pos=(940, 795), text_input="UNDO", font=get_font(45), base_color="White", hovering_color="Red")
        UNDO_BUTTON.changeColor(PLAY_MOUSE_POS)
        UNDO_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

                if UNDO_BUTTON.checkForInput(PLAY_MOUSE_POS) and len(history) >= 2:
                    # Nếu history có đủ ít nhất 2 nước đi (1 của X và 1 của O)
                    last_move_o = history.pop()  # Lấy nước đi của O
                    last_move_x = history.pop()  # Lấy nước đi của X

                    # Hoàn tác nước đi của O
                    row, col, player = last_move_o
                    board[row][col] = ""

                    # Hoàn tác nước đi của X
                    row, col, player = last_move_x
                    board[row][col] = ""

                    turn -= 2  # Quay lại lượt trước đó (đưa lượt về X nếu đang ở lượt O, hoặc ngược lại)

                else:
                    row, col = (PLAY_MOUSE_POS[1] - GRID_OFFSET_Y) // CELL_SIZE, (PLAY_MOUSE_POS[0] - GRID_OFFSET_X) // CELL_SIZE
                    if 0 <= row < N and 0 <= col < N and board[row][col] == "":
                        if current_mode_index == 0:  # Chế độ chơi với người (Player vs Player)
                            if turn % 2 == 0:  # Lượt của người chơi X
                                board[row][col] = "X"
                                history.append((row, col, "X"))  # Lưu nước đi của X
                                # Kiểm tra nếu người chơi X thắng
                                x_wins, winning_positions = check_winner(board, "X")
                                if x_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen(player_name)
                                    return
                            else:  # Lượt của người chơi O
                                board[row][col] = "O"
                                history.append((row, col, "O"))  # Lưu nước đi của O
                                # Kiểm tra nếu người chơi O thắng
                                o_wins, winning_positions = check_winner(board, "O")
                                if o_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen("O")
                                    return
                            turn += 1  # Sau mỗi lượt của X hoặc O, chúng ta tăng biến turn để chuyển lượt

                        elif current_mode_index == 1:  # Chế độ chơi với máy (Player vs Computer)
                            if turn % 2 == 0:  # Lượt của người chơi X
                                board[row][col] = "X"
                                history.append((row, col, "X"))  # Lưu nước đi của X
                                # Kiểm tra nếu người chơi X thắng
                                x_wins, winning_positions = check_winner(board, "X")
                                if x_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen(player_name)
                                    return
                                turn += 1  # Chuyển lượt sang O (máy)

                                # Máy đánh O (sau khi X đánh)
                                if turn % 2 == 1:  # Lượt của máy O
                                    row, col = find_random_empty_spot(board)
                                    if row is not None and col is not None:
                                        board[row][col] = "O"
                                        history.append((row, col, "O"))  # Lưu nước đi của O
                                        # Kiểm tra nếu máy O thắng
                                        o_wins, winning_positions = check_winner(board, "O")
                                        if o_wins:
                                            draw_symbols(SCREEN, board)
                                            draw_winning_line(SCREEN, winning_positions)
                                            pygame.display.update()
                                            pygame.time.delay(3000)
                                            display_winner_screen("O")
                                            return
                                        turn += 1  # Chuyển lượt sang X (người chơi)
        pygame.display.update()





        
def find_random_empty_spot(board):
    empty_spots = [(row, col) for row in range(len(board)) for col in range(len(board[0])) if board[row][col] == ""]
    return random.choice(empty_spots) if empty_spots else (None, None)

        
def display_winner_screen(winner):
    # Hỏi tên người chơi
    global player_name  # Đảm bảo biến toàn cục

    # Lưu kết quả vào bảng xếp hạng
    if winner == "X":
        save_score(player_name, "Lose")
    else:
        save_score(player_name, "Win")

    while True:
        SCREEN.blit(BG, (0, 0))  # Màu nền cho thông báo người thắng

        WINNER_TEXT = get_font(75).render(f"{winner} Wins!", True, "White")
        WINNER_RECT = WINNER_TEXT.get_rect(center=(670, 300))

        REPLAY_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(440, 500),
                               text_input="Replay", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(840, 500),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        SCORE_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 630),
                              text_input="Score", font=get_font(45), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(WINNER_TEXT, WINNER_RECT)

        for button in [REPLAY_BUTTON, BACK_BUTTON, SCORE_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    play()  # Bắt đầu lại trò chơi
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_menu()  # Quay lại menu chính
                if SCORE_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    display_leaderboard()  # Hiện bảng xếp hạng

        pygame.display.update()

# menu.py (Thêm hàm display_leaderboard)
def display_leaderboard():
    leaderboard = load_leaderboard()
    current_page = 0
    items_per_page = 10  # Giới hạn 10 mục trên mỗi trang

    while True:
        SCREEN.blit(BG, (0, 0))  # Đặt màu nền

        # Hiển thị tiêu đề bảng xếp hạng
        TITLE_TEXT = get_font(75).render("LEADERBOARD", True, "White")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        # Hiển thị các mục trên trang hiện tại
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page
        for index, entry in enumerate(leaderboard[start_index:end_index], start=start_index + 1):
            name_text = get_font(35).render(f"{index}. {entry[0]} - {entry[1]}", True, "White")
            name_rect = name_text.get_rect(center=(640, 150 + (index - start_index) * 50))
            SCREEN.blit(name_text, name_rect)

        # Nút "Previous" (Trang trước)
        prev_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(200, 650),
                             text_input="Pre", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        
        prev_button.changeColor(pygame.mouse.get_pos())
        prev_button.update(SCREEN)

        # Nút "Next" (Trang sau)
        next_button =  Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(1080, 650),
                             text_input="Next", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        next_button.changeColor(pygame.mouse.get_pos())
        next_button.update(SCREEN)

        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 750),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)

        # Kiểm tra sự kiện chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if prev_button.checkForInput(pygame.mouse.get_pos()) and current_page > 0:
                    current_page -= 1  # Chuyển về trang trước
                if next_button.checkForInput(pygame.mouse.get_pos()) and (current_page + 1) * items_per_page < len(leaderboard):
                    current_page += 1  # Chuyển đến trang sau
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return  # Trở về màn hình trước

        pygame.display.update()


# Hàm menu chính
# Hàm menu chính
def main_menu():
    global current_level_index, current_size_index,  player_name, current_mode_index
    input_active = False  # Kiểm tra xem ô nhập liệu có được chọn không
    cursor_visible = False  # Biến xác định con trỏ có hiển thị không
    last_cursor_toggle_time = 0  # Thời gian lần cuối cùng thay đổi trạng thái con trỏ nhấp nháy
    cursor_toggle_interval = 500  # Thời gian để chuyển đổi trạng thái con trỏ (500ms)

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CARO GAME", True, "White")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 570), 
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 720), 
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        LEFT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 300), 
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 300), 
                                   text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        LEVEL_TEXT = get_font(35).render(levels[current_level_index], True, "#d7fcd4")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 300))

        LEFT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 370), 
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 370), 
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        SIZE_TEXT = get_font(35).render(board_sizes[current_size_index], True, "#d7fcd4")
        SIZE_RECT = SIZE_TEXT.get_rect(center=(640, 370))
        
          # Thêm mũi tên điều chỉnh chế độ chơi (PLAYER vs COMPUTER)
        LEFT_ARROW_MODE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 440), 
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_MODE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 440), 
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        MODE_TEXT = get_font(35).render(mode[current_mode_index], True, "#d7fcd4")
        MODE_RECT = MODE_TEXT.get_rect(center=(640, 440))

        # Vẽ ô nhập tên người chơi với con trỏ nhấp nháy
        input_box = draw_input_box(SCREEN, 440, 200, 400, 50, player_name, get_font(35), "#d7fcd4", "White", cursor_visible)

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
        SCREEN.blit(SIZE_TEXT, SIZE_RECT)
        SCREEN.blit(MODE_TEXT, MODE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, LEFT_ARROW_LEVEL, RIGHT_ARROW_LEVEL, LEFT_ARROW_SIZE, RIGHT_ARROW_SIZE,LEFT_ARROW_MODE, RIGHT_ARROW_MODE]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Xử lý thay đổi trạng thái con trỏ nhấp nháy
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle_time > cursor_toggle_interval:
            cursor_visible = not cursor_visible  # Đổi trạng thái của con trỏ
            last_cursor_toggle_time = current_time  # Cập nhật thời gian

        # Sự kiện nhập liệu
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

                    
                if RIGHT_ARROW_SIZE.checkForInput(MENU_MOUSE_POS):
                    current_size_index = (current_size_index + 1) % len(board_sizes)

                # Chuyển đổi chế độ chơi giữa "PLAYER" và "COMPUTER"
                if LEFT_ARROW_MODE.checkForInput(MENU_MOUSE_POS):
                    current_mode_index = (current_mode_index - 1) % len(mode)
                if RIGHT_ARROW_MODE.checkForInput(MENU_MOUSE_POS):
                    current_mode_index = (current_mode_index + 1) % len(mode)

            # Nhận nhập liệu từ bàn phím
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]  # Xóa ký tự cuối cùng
                    else:
                        player_name += event.unicode  # Thêm ký tự vào tên
                # Kiểm tra xem có click vào ô nhập liệu không
                if input_box.collidepoint(MENU_MOUSE_POS):
                    input_active = True
                else:
                    input_active = False

        pygame.display.update()


main_menu()
