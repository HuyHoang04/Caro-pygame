import pygame
import sys
import random
import math


# Constants
SCREEN_SIZE = 600
GRID_SIZE = 15
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize board
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Gomoku: Player vs AI")

# Difficulty levels
EASY, MEDIUM, HARD, VERY_HARD = 1, 2, 3, 4
AI_DIFFICULTY = HARD  # Change this to EASY, MEDIUM, or HARD

def draw_board(screen, grid_size, cell_size):
    screen.fill(WHITE)
    for x in range(grid_size):
        pygame.draw.line(screen, BLACK, (x * cell_size, 0), (x * cell_size, SCREEN_SIZE))
        pygame.draw.line(screen, BLACK, (0, x * cell_size), (SCREEN_SIZE, x * cell_size))

def draw_stones(screen, board, grid_size, cell_size):
    for x in range(grid_size):
        for y in range(grid_size):
            if board[y][x] == 1:
                pygame.draw.circle(screen, BLACK, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 2)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, BLUE, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 2)

def check_winner(board, x, y, player, grid_size):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for dir in [1, -1]:
            nx, ny = x + dx * dir, y + dy * dir
            while 0 <= nx < grid_size and 0 <= ny < grid_size and board[ny][nx] == player:
                count += 1
                nx += dx * dir
                ny += dy * dir
            if count >= 5:
                return True
    return False
######################################################

def easy_ai_move(board, grid_size):
    empty_cells = [(x, y) for y in range(grid_size) for x in range(grid_size) if board[y][x] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        board[y][x] = 2
        return x, y
    return None
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
import random
import math

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
    # Check if the current player has won after the last move at (x, y)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    for dx, dy in directions:
        count = 1
        for i in range(1, 5):
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[ny][nx] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[ny][nx] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False


def block_move(board, player):
    # AI tries to block the opponent's winning move
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
                        board[y][x] = player  # Block the opponent's move
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
        board[y][x] = 2  # AI's move
        return x, y
    
    win_move = check_and_win(board, 2)
    if win_move:
        board[win_move[1]][win_move[0]] = 2  # AI đi vào vị trí thắng
        x,y = win_move[1],win_move[0]
        return x, y

        # Check and block before any further exploration if the opponent has a sequence to block
    bblock_move = check_and_block(board, 2, grid_size=GRID_SIZE)  # Check if the opponent (player 1) has a winning move
    if bblock_move:
        board[bblock_move[1]][bblock_move[0]] = 2  # AI places its piece to block the opponent
        x,y = bblock_move[1],bblock_move[0]
        return x, y

    # If no blocking move, use MCTS to decide the best move
    root = MCTSNode(board)
    best_move = mcts(root, simulations=3000)  # Simulate 100 iterations
    print("Best move:", best_move)
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

def initialize_game():
    return 1

def update_screen(screen, board, grid_size, cell_size):
    draw_board(screen, grid_size, cell_size)
    draw_stones(screen, board, grid_size, cell_size)
    pygame.display.flip()

def handle_player_turn(board, player):
    x, y = pygame.mouse.get_pos()
    x, y = x // CELL_SIZE, y // CELL_SIZE
    if player_move(board, x, y, player):
        return 2
    return player

def handle_ai_turn(board, grid_size, difficulty):
    move = ai_move(board, grid_size, difficulty)
    if move:
        x, y = move
        if check_winner(board, x, y, 2, grid_size):
            print("AI wins!")
            pygame.time.wait(2000)
            sys.exit()
    return 1

def main():
    player = initialize_game()
    running = True

    while running:
        update_screen(screen, board, GRID_SIZE, CELL_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player == 1:
                player = handle_player_turn(board, player)
                if player == 2:
                    player = handle_ai_turn(board, GRID_SIZE, AI_DIFFICULTY)

    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
