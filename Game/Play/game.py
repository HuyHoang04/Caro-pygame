import pygame
import sys
import random
import math
from button import Button
from leaderboard import save_score, load_leaderboard
from moviepy.editor import VideoFileClip

# Constants
SCREEN_SIZE = 1000
GRID_SIZE = 15 # N
CELL_SIZE = 600 // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLUE_LIGHT = (100, 149, 237) 
YELLOW_LIGHT = (255, 221, 51)  
RED = (180, 0, 0)
BACKGROUND_COLOR = pygame.image.load("assets/Background3.jpg")
ICON_X = pygame.image.load("assets/iconX.png")
ICON_O = pygame.image.load("assets/iconO.png")


# Điều chỉnh kích thước các icon sao cho vừa với ô bàn cờ
ICON_X = pygame.transform.scale(ICON_X, (CELL_SIZE - 4, CELL_SIZE - 4))
ICON_O = pygame.transform.scale(ICON_O, (CELL_SIZE - 4, CELL_SIZE - 4))
BG = pygame.image.load("assets/Background3.jpg")
frame_width = 3
# Initialize board
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Gomoku: Player vs AI")

# Sound
sound = pygame.mixer.Sound("assets/soundBG.mp3")
sound.set_volume(0.5)
# sound.play()

board_sizes = ["5x5", "8x8", "10x10", "15x15", "20x20"]
current_size_index = 2
mode = ["Player vs Player", "Player vs Computer", "Computer vs Computer"]
current_mode_index = 1
player_name = ""
player_1 = "X"
player_2 = "O"
ai_1 = "AI X"
ai_2 = "AI O"

history = []  # Danh sách lưu lịch sử các nước đi
# Difficulty levels
EASY, MEDIUM, HARD, VERY_HARD = 1, 2, 3, 4
levels = ["Easy", "Medium", "Hard", "Very Hard"]
current_level_index = 1

level_ai1 = ["Easy", "Medium", "Hard", "Very Hard"]
current_level_ai1 = 1
level_ai2 = ["Easy", "Medium", "Hard", "Very Hard"]
current_level_ai2 = 1
AI_DIFFICULTY = MEDIUM  # Change this to EASY, MEDIUM, or HARD


def intro(video_path="path/to/your/video.mp4"):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Intro Video")

    # Tải video bằng MoviePy
    clip = VideoFileClip(video_path)
    clip = clip.resize(height=SCREEN_SIZE, width=SCREEN_SIZE)

    # Lặp qua từng frame video và vẽ lên màn hình Pygame
    for frame in clip.iter_frames(fps=30, with_times=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
    
    clip.close()

def set_board_size(size):
    global GRID_SIZE, CELL_SIZE, board, ICON_X, ICON_O
    GRID_SIZE = size
    CELL_SIZE = 600 // GRID_SIZE  

    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    ICON_X = pygame.transform.scale(ICON_X, (CELL_SIZE - 4, CELL_SIZE - 4))
    ICON_O = pygame.transform.scale(ICON_O, (CELL_SIZE - 4, CELL_SIZE - 4))


def draw_board(screen, grid_size, cell_size, frame_width):
    screen.blit(BG, (0, 0))  
    start_x = (SCREEN_SIZE - 600) // 2  
    start_y = (SCREEN_SIZE - 600) // 2 

    pygame.draw.rect(screen, (0, 0, 0), (start_x, start_y, 600, 600))

    for x in range(grid_size + 1): 
        pygame.draw.line(screen, WHITE, 
                         (start_x + x * cell_size, start_y), 
                         (start_x + x * cell_size, start_y + 600), 
                         frame_width)  # Độ dày của các đường kẻ
        
   
        pygame.draw.line(screen, WHITE, 
                         (start_x, start_y + x * cell_size), 
                         (start_x + 600, start_y + x * cell_size), 
                         frame_width)



def draw_stones(screen, board, grid_size, cell_size):
    # Tính toán vị trí bắt đầu của bàn cờ để căn giữa
    start_x = (SCREEN_SIZE - 600) // 2
    start_y = (SCREEN_SIZE - 600) // 2

    for x in range(grid_size): 
        for y in range(grid_size):  
            if board[y][x] == 1: 
                screen.blit(
                    ICON_X,
                    (start_x + x * cell_size + 2, start_y + y * cell_size + 2)  
                )
            elif board[y][x] == 2:  
                screen.blit(
                    ICON_O,
                    (start_x + x * cell_size + 2, start_y + y * cell_size + 2)  
                )


def check_winner(board, x, y, player, grid_size):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Các hướng: ngang, dọc, chéo 1, chéo 2
    for dx, dy in directions:
        count = 1  
        for dir in [1, -1]:
            nx, ny = x + dx * dir, y + dy * dir
            while 0 <= nx < grid_size and 0 <= ny < grid_size and board[ny][nx] == player:
                count += 1
                nx += dx * dir
                ny += dy * dir
            if count >= 5:  # Nếu có 5 quân cờ liên tiếp
                return True
    return False


######################################################

def easy_ai_move(board, grid_size):
    # Tạo danh sách các ô trống
    empty_cells = [(x, y) for y in range(grid_size) for x in range(grid_size) if board[y][x] == 0]
    if empty_cells:
        # Chọn một ô trống ngẫu nhiên và đánh dấu "O"
        x, y = random.choice(empty_cells)
        board[y][x] = 2  # Máy tính đánh O (giả sử "O" là 2)
        return x, y  # Trả về vị trí x, y của ô mà máy tính đã chọn
    return None  # Nếu không có ô trống, trả về None

#############################################
def medium_ai_move(board, grid_size):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for y in range(grid_size):
        for x in range(grid_size):
            if board[y][x] == 0:
                for dx, dy in directions:
                    count = 0
                    open_ends = 0
                    
                    # Kiểm tra trong cả hai hướng để đếm số quân của người chơi liên tiếp
                    for dir in [1, -1]:
                        nx, ny = x + dx * dir, y + dy * dir
                        while 0 <= nx < grid_size and 0 <= ny < grid_size:
                            if board[ny][nx] == 1:
                                count += 1
                            elif board[ny][nx] == 0:
                                open_ends += 1
                                break
                            else:
                                break
                            nx += dx * dir
                            ny += dy * dir
                    
                    # Chặn khi có chuỗi 3 hoặc 4 quân liên tiếp với hai đầu trống
                    if (count == 3 and open_ends == 2) or (count == 4 and open_ends >= 1):
                        board[y][x] = 2
                        return x, y

    # Nếu không cần chặn, thực hiện nước đi ngẫu nhiên
    return easy_ai_move(board, grid_size)

###################################################

def evaluate_board(board):
    score = 0
    # Patterns to check:  
    patterns = {
        "open_four": 10000,   # Four in a row with both ends open
        "closed_four": 5000,  # Four in a row with one end open
        "open_three": 500,    # Three in a row with both ends open
        "closed_three": 100,  # Three in a row with one end open
        "open_two": 50,       # Two in a row with both ends open
        "closed_two": 10      # Two in a row with one end open
    }
    
    # Evaluate board for both players
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 2:  # AI stones
                score += evaluate_position(board, x, y, 2, patterns)
            elif board[y][x] == 1:  # Player stones
                score -= evaluate_position(board, x, y, 1, patterns)
    
    return score

def evaluate_position(board, x, y, player, patterns):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    position_score = 0

    for dx, dy in directions:
        count = 1
        open_ends = 0

        # Check in both directions
        for dir in [1, -1]:
            nx, ny = x + dx * dir, y + dy * dir
            while 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if board[ny][nx] == player:
                    count += 1
                elif board[ny][nx] == 0:
                    open_ends += 1
                    break
                else:
                    break
                nx += dx * dir
                ny += dy * dir

        # Assign scores based on pattern
        if count == 4 and open_ends == 2:
            position_score += patterns["open_four"]
        elif count == 4 and open_ends == 1:
            position_score += patterns["closed_four"]
        elif count == 3 and open_ends == 2:
            position_score += patterns["open_three"]
        elif count == 3 and open_ends == 1:
            position_score += patterns["closed_three"]
        elif count == 2 and open_ends == 2:
            position_score += patterns["open_two"]
        elif count == 2 and open_ends == 1:
            position_score += patterns["closed_two"]

    return position_score

# Minimax with Alpha-Beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board), None
    
    best_move = None
    if is_maximizing:
        max_eval = -math.inf
        for move in get_available_moves(board):
            x, y = move
            board[y][x] = 2  # AI move
            eval, _ = minimax(board, depth - 1, False, alpha, beta)
            board[y][x] = 0  # Undo move
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in get_available_moves(board):
            x, y = move
            board[y][x] = 1  # Player move
            eval, _ = minimax(board, depth - 1, True, alpha, beta)
            board[y][x] = 0  # Undo move
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Get all available moves
def get_available_moves(board):
    moves = []
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 0:
                moves.append((x, y))
    return moves

# Check if board state is terminal (win/loss/draw)
def is_terminal(board):
    # Check for a win
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] != 0:
                if check_winner(board, x, y, board[y][x], GRID_SIZE):
                    return True

    # Check if the board is full
    return all(cell != 0 for row in board for cell in row)


# Hard AI move function using Minimax with Alpha-Beta pruning
def hard_ai_move(board, grid_size):
    _, best_move = minimax(board, depth=2, is_maximizing=True, alpha=-math.inf, beta=math.inf)
    if best_move:
        x, y = best_move
        board[y][x] = 2
        return x, y
    return None

##############################################


class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board  # Current state of the board
        self.parent = parent
        self.move = move  # Move that led to this state
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = self.get_available_moves(board)

    def get_available_moves(self, board):
        # Get a list of all available moves (empty cells)
        return [(x, y) for x in range(len(board)) for y in range(len(board[0])) if board[y][x] == 0]

    def expand(self):
        # Expand the node by selecting an untried move and adding a new child
        move = self.untried_moves.pop()
        new_board = [row[:] for row in self.board]  # Make a copy of the board
        new_board[move[1]][move[0]] = 2  # AI's move (player 2)
        child_node = MCTSNode(new_board, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def best_child(self, exploration_weight=2.0):
        # UCB1 formula for selecting the best child
        return max(self.children, key=lambda c: c.wins / c.visits + exploration_weight * math.sqrt(math.log(self.visits) / c.visits))

    def update(self, result):
        self.visits += 1
        self.wins += result  # Update wins with 1 for win, 0 for loss/tie


def check_win(board, player, x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1  # Đếm quân cờ hiện tại tại (x, y)

        # Kiểm tra theo hướng (dx, dy)
        for i in range(1, 5):  # Kiểm tra 4 quân cờ tiếp theo theo hướng (dx, dy)
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[ny][nx] == player:
                count += 1
            else:
                break

        # Kiểm tra theo hướng ngược lại (-dx, -dy)
        for i in range(1, 5):  # Kiểm tra 4 quân cờ tiếp theo theo hướng ngược lại (-dx, -dy)
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[ny][nx] == player:
                count += 1
            else:
                break

        # Nếu có ít nhất 5 quân cờ liên tiếp theo một hướng, trả về True
        if count >= 5:
            return True

    return False



def block_move(board, player):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[y][x] == 0:
                # Simulate a move by the opponent
                board[y][x] = player
                if check_win(board, player, x, y):  # Check if the opponent wins
                    return x, y  # Block the winning move
                board[y][x] = 0  # Undo the move
    return None  # No immediate blocking needed


def simulate_random_game(board):
    # Simulate a random game from the current board state, returning 1 if AI wins, 0 otherwise
    grid_size = len(board)
    current_board = [row[:] for row in board]
    current_player = 2
    available_moves = [(x, y) for x in range(grid_size) for y in range(grid_size) if current_board[y][x] == 0]

    while available_moves:
        move = random.choice(available_moves)
        current_board[move[1]][move[0]] = current_player

        if check_win(current_board, current_player, move[0], move[1]):
            return 1 if current_player == 2 else 0

        current_player = 3 - current_player  # Switch player

    return 0  # No winner


def check_and_block(board, player, grid_size):
    """
    This function checks if the opponent has a sequence of 3 or 4 consecutive stones
    with one or two open ends and returns the position where the AI should block (if any).
    """
    opponent = 1 if player == 2 else 2  # The opponent is the other player
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Right, Down, Diagonal Down-Right, Diagonal Up-Right

    for y in range(grid_size):
        for x in range(grid_size):
            if board[y][x] == 0:  # Check only empty spots
                for dx, dy in directions:
                    count = 0
                    open_ends = 0

                    # Check in both directions for a potential sequence of 3 or 4 with open ends
                    for dir in [1, -1]:
                        nx, ny = x + dx * dir, y + dy * dir
                        while 0 <= nx < grid_size and 0 <= ny < grid_size:
                            if board[ny][nx] == opponent:
                                count += 1
                            elif board[ny][nx] == 0:
                                open_ends += 1
                                break
                            else:
                                break
                            nx += dx * dir
                            ny += dy * dir
                    
                    # Block when there are 3 or 4 consecutive opponent stones with open ends
                    # A sequence of 3 with 2 open ends or 4 with at least 1 open end should be blocked
                    if (count == 3 and open_ends == 2) or (count == 4 and open_ends >= 1):
                
                        print("blocked", x, y, open_ends)
                        return x, y  # Return the position of the block

    return None  
def check_and_win(board, player):
    """
    Kiểm tra nếu AI có thể thắng ngay lập tức bằng cách đi vào một ô trống sau chuỗi 4 quân liên tiếp.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 0:  # Tìm ô trống mà AI có thể đi
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    count = 1
                    open_ends = 0

                    # Kiểm tra 2 chiều cho chuỗi 4 quân liên tiếp với 1 ô trống
                    for dir in [1, -1]:
                        nx, ny = x + dx * dir, y + dy * dir
                        while 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            if board[ny][nx] == player:
                                count += 1
                            elif board[ny][nx] == 0:
                                open_ends += 1
                                break
                            else:
                                break
                            nx += dx * dir
                            ny += dy * dir

                    # Nếu có 4 quân liên tiếp và 1 ô trống, AI có thể thắng
                    if count == 4 and open_ends == 1:
                        return x, y  # Nước đi thắng ngay lập tức

    return None  # Không có cơ hội thắng ngay lập tức

def mcts(root, simulations, player=2):
    """
    Perform MCTS search with defense logic to block the opponent's moves.
    """
    for _ in range(simulations):
        node = root
        

        # If no immediate blocking move is required, proceed with normal MCTS steps
        while node.untried_moves == [] and node.children:
            node = node.best_child()

        if node.untried_moves:
            node = node.expand()

        result = evaluate_board(node.board)  # Evaluate the board after a move

        while node is not None:
            node.update(result)
            node = node.parent

    return root.best_child(exploration_weight=0).move  # Return the best move for AI


# AI move function
def very_hard_ai_move(board):
    # First, try to block the opponent's winning move
    block = block_move(board, 1)  # 1 is the opponent's player
    if block:
        print("Blocking move:", block)
        x, y = block
        
        return x, y
    
    win_move = check_and_win(board, 2)
    if win_move:
          # AI đi vào vị trí thắng
        x,y = win_move[1],win_move[0]
        return x, y

        # Check and block before any further exploration if the opponent has a sequence to block
    bblock_move = check_and_block(board, 2, grid_size=GRID_SIZE)  # Check if the opponent (player 1) has a winning move
    if bblock_move:
          # AI places its piece to block the opponent
        x,y = bblock_move[1],bblock_move[0]
    
        return x, y

    # If no blocking move, use MCTS to decide the best move
    root = MCTSNode(board)
    best_move = mcts(root, simulations=3000)
    print("Best move:", best_move)# Simulate 100 iterations
    x, y = best_move
    board[y][x] = 2  # AI's move
    return x, y
##############
def ai_move(board, grid_size, difficulty):
    if difficulty == EASY:
        return easy_ai_move(board, grid_size)
    elif difficulty == MEDIUM:
        return medium_ai_move(board, grid_size)
    elif difficulty == HARD:
        return hard_ai_move(board, grid_size)
    elif difficulty == VERY_HARD:
        return very_hard_ai_move(board)  # You can adjust the number of simulations
    return None


def player_move(board, x, y, player):
    if board[y][x] == 0:
        board[y][x] = player
        if check_winner(board, x, y, player, GRID_SIZE):
            print("Player wins!")
            pygame.time.wait(2000)
            sys.exit()
        return True
    return False

def display_winner_screen(winner):
    global player_name, player_1, player_2, current_mode_index, ai_1, ai_2

    if current_mode_index == 1:  
        if winner == 2:
            save_score(player_name, "Lose")
            winner_text = "AI Wins!"
        else:
            save_score(player_name, "Win")
            winner_text = f"{player_name} Wins!"
    elif current_mode_index == 0: 
        if winner == player_1:
            winner_text = f"{player_1} Wins!"
        elif winner == player_2:
            winner_text = f"{player_2} Wins!"
    elif current_mode_index == 2: 
        if winner == ai_1:
            winner_text = f"{ai_1} Wins!"
        elif winner == ai_2:
            winner_text = f"{ai_2} Wins!"

    while True:
        screen.blit(BG, (0, 0))  

        WINNER_TEXT = get_font(75).render(winner_text, True, "White")
        WINNER_RECT = WINNER_TEXT.get_rect(center=(SCREEN_SIZE // 2, 300))
        screen.blit(WINNER_TEXT, WINNER_RECT)

        REPLAY_BUTTON = Button(
            image=pygame.image.load("assets/Quit Rect.png"), 
            pos=(300, 500),
            text_input="Replay", 
            font=get_font(45), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )
        BACK_BUTTON = Button(
            image=pygame.image.load("assets/Quit Rect.png"), 
            pos=(750, 500),
            text_input="BACK", 
            font=get_font(45), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )
        SCORE_BUTTON = Button(
            image=pygame.image.load("assets/Quit Rect.png"), 
            pos=(SCREEN_SIZE // 2, 660),
            text_input="Score", 
            font=get_font(45), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

        for button in [REPLAY_BUTTON, BACK_BUTTON, SCORE_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    global board
                    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Reset board
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
        screen.blit(BG, (0, 0))  
        TITLE_TEXT = get_font(65).render("LEADERBOARD", True, "White")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(SCREEN_SIZE//2, 100))
        screen.blit(TITLE_TEXT, TITLE_RECT)
        start_index = current_page * items_per_page
        end_index = start_index + items_per_page
        for index, entry in enumerate(leaderboard[start_index:end_index], start=start_index + 1):
            name_text = get_font(35).render(f"{index}. {entry[0]} - {entry[1]}", True, "White")
            name_rect = name_text.get_rect(center=(SCREEN_SIZE//2, 150 + (index - start_index) * 50))
            screen.blit(name_text, name_rect)

        PREV_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(300, 880),
                             text_input="Pre", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        PREV_BUTTON.changeColor(pygame.mouse.get_pos())
        PREV_BUTTON.update(screen)

        NEXT_BUTTON =  Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(710, 880),
                             text_input="Next", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        NEXT_BUTTON.changeColor(pygame.mouse.get_pos())
        NEXT_BUTTON.update(screen)
        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_SIZE//2, 750),
                             text_input="BACK", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(screen)


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

def initialize_game():
    global board, current_player, game_over
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = 1 
    game_over = False  


def update_screen(screen, board, grid_size, cell_size):
    draw_board(screen, grid_size, cell_size, frame_width)
    draw_stones(screen, board, grid_size, cell_size)


def handle_player_turn(board, player):
    global player_name, history, player_1, player_2, current_mode_index
    x, y = pygame.mouse.get_pos()

    x = (x - (SCREEN_SIZE - 600) // 2) // CELL_SIZE
    y = (y - (SCREEN_SIZE - 600) // 2) // CELL_SIZE
    
    if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
        return player  

    # Kiểm tra nếu ô này còn trống
    if board[y][x] == 0:
        board[y][x] = player 
        history.append((x, y))  


        if player == 1:
            screen.blit(ICON_X, 
                        (x * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2, 
                         y * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2))
        elif player == 2:
            screen.blit(ICON_O, 
                        (x * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2, 
                         y * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2))
        pygame.display.update()  
        
        if check_winner(board, x, y, player, GRID_SIZE):
            if current_mode_index == 1:  
                if player == 1:
                    display_winner_screen(player_name)  
                elif player == 2:
                    display_winner_screen("Player 2")  
            else:  
                if player == 1:
                    display_winner_screen(player_1)  
                elif player == 2:
                    display_winner_screen(player_2)  
            pygame.time.wait(2000)  
            sys.exit()  

        return 3 - player  

    return player  





def handle_ai_turn(board, grid_size, difficulty):
    global history
    move = ai_move(board, grid_size, difficulty)

    if move:
        x, y = move
        board[y][x] = 2 
        history.append((x, y))  

        screen.blit(ICON_O, 
                    (x * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2, 
                     y * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2))
        pygame.display.update() 
        
        if check_winner(board, x, y, 2, grid_size):
            display_winner_screen("AI")
            save_score(player_name, "Lose") 
            pygame.time.wait(2000)
            sys.exit()

    return 1  


def handle_ai_ai_turn(board, grid_size):
    global history, ai_1, ai_2
    
    # Ánh xạ cấp độ AI sang các hàm AI tương ứng cho AI 1
    if level_ai1[current_level_ai1] == "Easy":
        move_1 = easy_ai_move(board, grid_size)
    elif level_ai1[current_level_ai1] == "Medium":
        move_1 = medium_ai_move(board, grid_size)
    elif level_ai1[current_level_ai1] == "Hard":
        move_1 = hard_ai_move(board, grid_size)
    elif level_ai1[current_level_ai1] == "Very Hard":
        move_1 = very_hard_ai_move(board, grid_size)

    if move_1:
        x, y = move_1
        board[y][x] = 1
        history.append(((x, y)))  # Lưu nước đi của AI 1

        screen.blit(ICON_X, (x * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2, y * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2))
        pygame.display.update()  

        if check_winner(board, x, y, 1, grid_size):
            display_winner_screen(ai_1) 
            pygame.time.wait(2000)
            sys.exit()  

    # Cập nhật cho AI 2
    if level_ai2[current_level_ai2] == "Easy":
        move_2 = easy_ai_move(board, grid_size)
    elif level_ai2[current_level_ai2] == "Medium":
        move_2 = medium_ai_move(board, grid_size)
    elif level_ai2[current_level_ai2] == "Hard":
        move_2 = hard_ai_move(board, grid_size)
    elif level_ai2[current_level_ai2] == "Very Hard":
        move_2 = very_hard_ai_move(board, grid_size)

    if move_2:
        x, y = move_2
        board[y][x] = 2
        history.append(((x, y)))  # Lưu nước đi của AI 2

        screen.blit(ICON_O, (x * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2, y * CELL_SIZE + (SCREEN_SIZE - 600) // 2 + 2))
        pygame.display.update()  

        if check_winner(board, x, y, 2, grid_size):
            display_winner_screen(ai_2)  
            pygame.time.wait(2000)
            sys.exit()  

    return 1





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

                
def main_menu():
    global current_level_index, current_size_index, player_name, current_mode_index, AI_DIFFICULTY
    cursor_visible = True
    input_active = False
    last_cursor_toggle_time = pygame.time.get_ticks()
    cursor_toggle_interval = 500  

    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Main Title
        MENU_TEXT = get_font(50).render("CARO GAME", True, "White")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_SIZE // 2, 120))

        # Buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_SIZE // 2, 570),
                             text_input="PLAY", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        SCORE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_SIZE // 2, 720),
                              text_input="SCORE", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_SIZE // 2, 870),
                             text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

       
        LEFT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(300, 300),
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        RIGHT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(700, 300),
                                   text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        LEVEL_TEXT = get_font(35).render(levels[current_level_index], True, "#d7fcd4")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(SCREEN_SIZE // 2, 300))

       
        LEFT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(330, 370),
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        RIGHT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(670, 370),
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        SIZE_TEXT = get_font(35).render(board_sizes[current_size_index], True, "#d7fcd4")
        SIZE_RECT = SIZE_TEXT.get_rect(center=(SCREEN_SIZE // 2, 370))

        
        LEFT_ARROW_MODE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(110, 440),
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        RIGHT_ARROW_MODE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(880, 440),
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        MODE_TEXT = get_font(35).render(mode[current_mode_index], True, "#d7fcd4")
        MODE_RECT = MODE_TEXT.get_rect(center=(SCREEN_SIZE // 2, 440))

        input_box = draw_input_box(screen, 250, 180, 500, 50, player_name, get_font(35), "#d7fcd4", "White", cursor_visible)

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(LEVEL_TEXT, LEVEL_RECT)
        screen.blit(SIZE_TEXT, SIZE_RECT)
        screen.blit(MODE_TEXT, MODE_RECT)

        for button in [PLAY_BUTTON, SCORE_BUTTON, QUIT_BUTTON, LEFT_ARROW_LEVEL, RIGHT_ARROW_LEVEL,
                       LEFT_ARROW_SIZE, RIGHT_ARROW_SIZE, LEFT_ARROW_MODE, RIGHT_ARROW_MODE]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

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
                    if current_mode_index == 2:  # "Computer vs Computer"
                        choose_level_ai()  # Go to AI level selection screen
                    else:
                        play()  # Start the game directly for other modes
                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    display_leaderboard()  
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

            # Handle player name input
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif len(player_name) < 10:  # Limit to 10 characters
                        player_name += event.unicode
                if input_box.collidepoint(MENU_MOUSE_POS):
                    input_active = True
                else:
                    input_active = False

        # Update AI_DIFFICULTY
        AI_DIFFICULTY = [EASY, MEDIUM, HARD, VERY_HARD][current_level_index]

        pygame.display.update()


def choose_level_ai():
    global current_level_ai1, current_level_ai2, AI_DIFFICULTY
    cursor_visible = True
    last_cursor_toggle_time = pygame.time.get_ticks()
    cursor_toggle_interval = 500  
    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Main Title
        MENU_TEXT = get_font(30).render("Please Choose AI Level", True, YELLOW_LIGHT)
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_SIZE // 2, 120))

        # Buttons
        DONE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_SIZE // 2, 610),
                             text_input="DONE", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_SIZE // 2, 790),
                             text_input="BACK", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

       
        AI1_TEXT = get_font(30).render("AI X", True, BLUE_LIGHT)
        AI1_RECT = AI1_TEXT.get_rect(center=(SCREEN_SIZE // 2, 240))
        
        LEFT_ARROW_LEVEL_AI1 = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(300, 300),
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        RIGHT_ARROW_LEVEL_AI1 = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(700, 300),
                                   text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        LEVEL_AI1_TEXT = get_font(35).render(level_ai1[current_level_ai1], True, "#d7fcd4")
        LEVEL_AI1_RECT = LEVEL_AI1_TEXT.get_rect(center=(SCREEN_SIZE // 2, 300))
        
        AI2_TEXT = get_font(30).render("AI O", True, RED)
        AI2_RECT = AI2_TEXT.get_rect(center=(SCREEN_SIZE // 2, 380))
        
        LEFT_ARROW_LEVEL_AI2 = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(300, 440),
                                 text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        RIGHT_ARROW_LEVEL_AI2 = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(700, 440),
                                  text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        LEVEL_AI2_TEXT = get_font(35).render(level_ai2[current_level_ai2], True, "#d7fcd4")
        LEVEL_AI2_RECT = LEVEL_AI2_TEXT.get_rect(center=(SCREEN_SIZE // 2, 440))


        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(AI1_TEXT, AI1_RECT)
        screen.blit(AI2_TEXT, AI2_RECT)
        screen.blit(LEVEL_AI1_TEXT, LEVEL_AI1_RECT)
        screen.blit(LEVEL_AI2_TEXT, LEVEL_AI2_RECT)

        for button in [DONE_BUTTON, BACK_BUTTON, LEFT_ARROW_LEVEL_AI1, RIGHT_ARROW_LEVEL_AI1,
                        LEFT_ARROW_LEVEL_AI2, RIGHT_ARROW_LEVEL_AI2]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_toggle_time > cursor_toggle_interval:
            cursor_visible = not cursor_visible
            last_cursor_toggle_time = current_time
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DONE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()  # Start the game after selecting AI level
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if LEFT_ARROW_LEVEL_AI1.checkForInput(MENU_MOUSE_POS):
                    current_level_ai1 = (current_level_ai1 - 1) % len(level_ai1)
                if RIGHT_ARROW_LEVEL_AI1.checkForInput(MENU_MOUSE_POS):
                    current_level_ai1 = (current_level_ai1 + 1) % len(level_ai1)
                if LEFT_ARROW_LEVEL_AI2.checkForInput(MENU_MOUSE_POS):
                    current_level_ai2 = (current_level_ai2 - 1) % len(level_ai2)
                if RIGHT_ARROW_LEVEL_AI2.checkForInput(MENU_MOUSE_POS):
                    current_level_ai2 = (current_level_ai2 + 1) % len(level_ai2)
            
            

        # Update AI_DIFFICULTY
        AI_DIFFICULTY = [EASY, MEDIUM, HARD, VERY_HARD][current_level_index]

        pygame.display.update()
def undo():
    global history, board, current_mode_index

    if current_mode_index == 2:
        if len(history) >= 2:  

            last_move_ai_2 = history.pop() 
            last_move_ai_1 = history.pop() 
            board[last_move_ai_1[1]][last_move_ai_1[0]] = 0  
            board[last_move_ai_2[1]][last_move_ai_2[0]] = 0 
            update_screen(screen, board, GRID_SIZE, CELL_SIZE)
            pygame.display.update()

    else:
      
        if len(history) >= 2:  
            last_move_player = history.pop()  
            last_move_ai = history.pop() 
            board[last_move_player[1]][last_move_player[0]] = 0 
            board[last_move_ai[1]][last_move_ai[0]] = 0  
            update_screen(screen, board, GRID_SIZE, CELL_SIZE)
            pygame.display.update()




def play():
    global player_name, board, GRID_SIZE, current_player, game_over, history, current_mode_index

    player = initialize_game()  
    board_size = int(board_sizes[current_size_index].split('x')[0])
    GRID_SIZE = board_size
    set_board_size(board_size)

    # Các nút trong game
    if current_mode_index == 2:
        REPLAY = Button(image=pygame.image.load("assets/Quit Rect.png"), 
                           pos=(SCREEN_SIZE//2, 890),  # Căn giữa nút BACK
                           text_input="REPLAY", font=get_font(45), base_color="White", hovering_color="Red")
    else:
        REPLAY = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(240, 890), text_input="REPLAY", font=get_font(45), base_color="White", hovering_color="Red")
    
    PLAY_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), 
                           pos=(240, 110),  # Vị trí mặc định của nút BACK
                           text_input="BACK", font=get_font(45), base_color="White", hovering_color="Red")

    if current_mode_index != 2:  
        UNDO_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(780, 890), text_input="UNDO", font=get_font(45), base_color="White", hovering_color="Red")
    else:
        UNDO_BUTTON = None  

    history = []  
    current_player = 1  
    game_over = False  
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill((0, 2, 0)) 
        update_screen(screen, board, GRID_SIZE, CELL_SIZE)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        REPLAY.changeColor(PLAY_MOUSE_POS)
        REPLAY.update(screen)

        if UNDO_BUTTON:
            UNDO_BUTTON.changeColor(PLAY_MOUSE_POS)
            UNDO_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):  
                    if current_mode_index == 2: 
                        choose_level_ai() 
                    else:
                        main_menu()  

                if UNDO_BUTTON and UNDO_BUTTON.checkForInput(PLAY_MOUSE_POS) and len(history) >= 2:
                    undo()  

                if REPLAY.checkForInput(PLAY_MOUSE_POS):
                    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  
                    history = [] 
                    current_player = 1  
                    game_over = False  
                    play() 

                if not game_over:  
                    if current_mode_index == 0:  
                        if current_player == 1:
                            current_player = handle_player_turn(board, current_player)  
                        elif current_player == 2:
                            current_player = handle_player_turn(board, current_player)  

                    elif current_mode_index == 1:  
                        if current_player == 1:
                            current_player = handle_player_turn(board, current_player)  
                        if current_player == 2:
                            current_player = handle_ai_turn(board, GRID_SIZE, AI_DIFFICULTY)  

                    elif current_mode_index == 2: 
                        if not game_over:
                            handle_ai_ai_turn(board, GRID_SIZE)  

        pygame.display.update() 




def main():
    """Khởi động game từ menu chính."""
    # intro("./assets/intro.mp4")
    main_menu()
   

if __name__ == "__main__":
    main()
