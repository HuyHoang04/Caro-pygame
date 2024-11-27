import pygame, sys, random, pyperclip

# Thiết lập các biến và hằng số
pygame.init()

N = 18
WIN_CONDITION = 5
CELL_SIZE = 35
WIDTH = 1000
HEIGHT = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = pygame.image.load("assets/Background3.jpg")
LINE_WIDTH = 2
FRAME_COLOR = (0, 128, 128)
FRAME_WIDTH = 6
board_sizes = ["8x8", "10x10", "15x15", "18x18"]
current_size_index = 2

levels = ["Easy", "Medium","Hard"]
current_level_index = 1

mode = ["Player vs Player", "Player vs Computer"]
current_mode_index = 0

# Tải các biểu tượng X và O
ICON_X = pygame.image.load("assets/iconX.png")
ICON_O = pygame.image.load("assets/iconO.png")
ICON_X = pygame.transform.scale(ICON_X, (CELL_SIZE - 10, CELL_SIZE - 10))
ICON_O = pygame.transform.scale(ICON_O, (CELL_SIZE - 10, CELL_SIZE - 10))

# Các chức năng hỗ trợ
def update_grid_offset():
    global GRID_OFFSET_X, GRID_OFFSET_Y
    total_width = N * CELL_SIZE
    total_height = N * CELL_SIZE
    GRID_OFFSET_X = (WIDTH - total_width) // 4
    GRID_OFFSET_Y = (HEIGHT - total_height) // 4

def set_board_size(size):
    global N
    N = size
    update_grid_offset()

def get_board_size():
    return N

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

def draw_grid(screen):
    """
    Vẽ lưới bàn cờ vào màn hình.
    """
    screen.blit(BACKGROUND_COLOR, (0, 0))
    pygame.draw.rect(screen, FRAME_COLOR, (GRID_OFFSET_X - FRAME_WIDTH, GRID_OFFSET_Y - FRAME_WIDTH, N * CELL_SIZE + 2 * FRAME_WIDTH, N * CELL_SIZE + 2 * FRAME_WIDTH))
    pygame.draw.rect(screen, BLACK, (GRID_OFFSET_X, GRID_OFFSET_Y, N * CELL_SIZE, N * CELL_SIZE))

    for i in range(1, N):
        pygame.draw.line(screen, WHITE, (GRID_OFFSET_X, GRID_OFFSET_Y + CELL_SIZE * i), (GRID_OFFSET_X + N * CELL_SIZE, GRID_OFFSET_Y + CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y), (GRID_OFFSET_X + CELL_SIZE * i, GRID_OFFSET_Y + N * CELL_SIZE), LINE_WIDTH)

def draw_symbols(screen, board):
    """
    Vẽ các ký hiệu "X" và "O" vào bàn cờ.
    """
    for row in range(N):
        for col in range(N):
            if board[row][col] == "X":
                screen.blit(ICON_X, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))
            elif board[row][col] == "O":
                screen.blit(ICON_O, (GRID_OFFSET_X + col * CELL_SIZE + 5, GRID_OFFSET_Y + row * CELL_SIZE + 5))

def draw_winning_line(screen, positions):
    if not positions:
        return
    start_pos = positions[0]
    end_pos = positions[-1]
    start_x = GRID_OFFSET_X + start_pos[1] * CELL_SIZE + CELL_SIZE // 2
    start_y = GRID_OFFSET_Y + start_pos[0] * CELL_SIZE + CELL_SIZE // 2
    end_x = GRID_OFFSET_X + end_pos[1] * CELL_SIZE + CELL_SIZE // 2
    end_y = GRID_OFFSET_Y + end_pos[0] * CELL_SIZE + CELL_SIZE // 2

    # Vẽ đường thắng
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), LINE_WIDTH * 2)

# Các phần còn lại của chương trình (menu, chơi game, v.v.)
from button import Button
from checkwin import check_winner
from leaderboard import save_score, load_leaderboard

SCREEN = pygame.display.set_mode((1280, 850))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background3.jpg")
sound = pygame.mixer.Sound("assets/soundBG.mp3")
sound.set_volume(0.5)
sound.play()
button_click_sound = pygame.mixer.Sound("assets/buttonclick.mp3")
player_name = ""

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def draw_input_box(SCREEN, x, y, width, height, text, font, base_color, active_color, cursor_visible):
    input_box = pygame.Rect(x, y, width, height)
    pygame.draw.rect(SCREEN, base_color, input_box) 
    text_surface = font.render(text, True, (0, 0, 0))  
    text_rect = text_surface.get_rect(center=input_box.center)  
    SCREEN.blit(text_surface, text_rect)
    if cursor_visible:
        cursor_rect = pygame.Rect(text_rect.right + 5, text_rect.top, 2, text_rect.height)
        pygame.draw.rect(SCREEN, (0, 0, 0), cursor_rect) 
    return input_box

# Các hàm game play, main menu, display winner, display leaderboard v.v...
def play():
    global player_name
    board_size = int(board_sizes[current_size_index].split('x')[0]) 
    global N
    N = board_size
    board = [["" for _ in range(N)] for _ in range(N)]
    set_board_size(board_size)
    history = [] 
    turn = 0

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        draw_grid(SCREEN)
        draw_symbols(SCREEN, board)
        PLAY_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(1030, 560), text_input="BACK", font=get_font(45), base_color="White", hovering_color="Red")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        UNDO_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(1030, 695), text_input="UNDO", font=get_font(45), base_color="White", hovering_color="Red")
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
                    last_move_o = history.pop()
                    last_move_x = history.pop()
                    row, col, player = last_move_o
                    board[row][col] = ""
                    row, col, player = last_move_x
                    board[row][col] = ""
                    turn -= 2
                else:
                    row, col = (PLAY_MOUSE_POS[1] - GRID_OFFSET_Y) // CELL_SIZE, (PLAY_MOUSE_POS[0] - GRID_OFFSET_X) // CELL_SIZE
                    if 0 <= row < N and 0 <= col < N and board[row][col] == "":
                        if current_mode_index == 0:  # Player vs Player
                            if turn % 2 == 0:  # Người chơi đánh X
                                board[row][col] = "X"
                                history.append((row, col, "X"))
                                x_wins, winning_positions = check_winner(board, "X")
                                if x_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen(player_name)
                                    return
                            else:  # Người chơi đánh O
                                board[row][col] = "O"
                                history.append((row, col, "O"))
                                o_wins, winning_positions = check_winner(board, "O")
                                if o_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen("O")
                                    return
                            turn += 1
                        elif current_mode_index == 1:  # Player vs Computer
                            if turn % 2 == 0:  # Người chơi đánh X
                                board[row][col] = "X"
                                history.append((row, col, "X"))
                                x_wins, winning_positions = check_winner(board, "X")
                                if x_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen(player_name)
                                    return
                                turn += 1  # Chuyển lượt
                                
                                # Máy đánh O ngay lập tức sau khi người chơi đánh X
                                row, col = get_random_empty_cell(board)  # Hàm này sẽ tìm ô trống cho máy
                                board[row][col] = "O"
                                history.append((row, col, "O"))
                                o_wins, winning_positions = check_winner(board, "O")
                                if o_wins:
                                    draw_symbols(SCREEN, board)
                                    draw_winning_line(SCREEN, winning_positions)
                                    pygame.display.update()
                                    pygame.time.delay(1500)
                                    display_winner_screen("O")
                                    return
                                turn += 1  # Chuyển lượt
        pygame.display.update()




        
def find_random_empty_spot(board):
    empty_spots = [(row, col) for row in range(len(board)) for col in range(len(board[0])) if board[row][col] == ""]
    return random.choice(empty_spots) if empty_spots else (None, None)

        
def display_winner_screen(winner):
    global player_name  
    if winner == "X":
        save_score(player_name, "Lose")
    else:
        save_score(player_name, "Win")

    while True:
        SCREEN.blit(BG, (0, 0))  
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
                  
                    play()  
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                   
                    main_menu()  
                if SCORE_BUTTON.checkForInput(pygame.mouse.get_pos()):
                   
                    display_leaderboard() 
        pygame.display.update()

def display_leaderboard():
    leaderboard = load_leaderboard()
    current_page = 0
    items_per_page = 10  # Giới hạn 10 mục trên mỗi trang

    while True:
        SCREEN.blit(BG, (0, 0))  
        TITLE_TEXT = get_font(75).render("LEADERBOARD", True, "White")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page
        for index, entry in enumerate(leaderboard[start_index:end_index], start=start_index + 1):
            name_text = get_font(35).render(f"{index}. {entry[0]} - {entry[1]}", True, "White")
            name_rect = name_text.get_rect(center=(640, 150 + (index - start_index) * 50))
            SCREEN.blit(name_text, name_rect)

        PREV_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(200, 650),
                             text_input="Pre", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        PREV_BUTTON.changeColor(pygame.mouse.get_pos())
        PREV_BUTTON.update(SCREEN)

        NEXT_BUTTON =  Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(1080, 650),
                             text_input="Next", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON.changeColor(pygame.mouse.get_pos())
        NEXT_BUTTON.update(SCREEN)
        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 750),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PREV_BUTTON.checkForInput(pygame.mouse.get_pos()) and current_page > 0:
                    
                    current_page -= 1 
                if NEXT_BUTTON.checkForInput(pygame.mouse.get_pos()) and (current_page + 1) * items_per_page < len(leaderboard):
                   
                    current_page += 1  
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                   
                    return  

        pygame.display.update()



def main_menu():
    global current_level_index, current_size_index,  player_name, current_mode_index
    input_active = False 
    cursor_visible = False  
    last_cursor_toggle_time = 0  
    cursor_toggle_interval = 500  

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
        
          
        LEFT_ARROW_MODE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(260, 440), 
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        RIGHT_ARROW_MODE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(1000, 440), 
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        MODE_TEXT = get_font(35).render(mode[current_mode_index], True, "#d7fcd4")
        MODE_RECT = MODE_TEXT.get_rect(center=(640, 440))

       #Nhập tên người chơi
        input_box = draw_input_box(SCREEN, 440, 200, 400, 50, player_name, get_font(35), "#d7fcd4", "White", cursor_visible)

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
        SCREEN.blit(SIZE_TEXT, SIZE_RECT)
        SCREEN.blit(MODE_TEXT, MODE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, LEFT_ARROW_LEVEL, RIGHT_ARROW_LEVEL, LEFT_ARROW_SIZE, RIGHT_ARROW_SIZE,LEFT_ARROW_MODE, RIGHT_ARROW_MODE]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle_time > cursor_toggle_interval:
            cursor_visible = not cursor_visible 
            last_cursor_toggle_time = current_time  

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


                if RIGHT_ARROW_SIZE.checkForInput(MENU_MOUSE_POS):
                   
                    current_size_index = (current_size_index + 1) % len(board_sizes)
                    set_board_size(int(board_sizes[current_size_index].split('x')[0]))


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