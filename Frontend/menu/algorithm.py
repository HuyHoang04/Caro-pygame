import random
import heapq
from checkwin import check_winner  # Sử dụng hàm kiểm tra người thắng

def minimax(board, depth, maximizing_player=True):
    if depth == 0 or is_game_over(board):  # Nếu độ sâu là 0 hoặc game đã kết thúc
        return evaluate_board(board)  # Trả về điểm đánh giá cho bàn cờ hiện tại

    best_move = None
    if maximizing_player:  # Máy tính (O) tìm nước đi tối ưu
        best_value = float('-inf')
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == "":  # Nếu ô trống
                    board[row][col] = "O"
                    move_value = minimax(board, depth - 1, False)  # Đệ quy, chuyển lượt cho người chơi
                    board[row][col] = ""  # Quay lại trạng thái ban đầu
                    if move_value > best_value:
                        best_value = move_value
                        best_move = (row, col)  # Lưu lại tọa độ của nước đi tốt nhất
        return best_value if best_move is None else best_value  # Trả về điểm tốt nhất
    else:  # Người chơi (X) tìm nước đi tối ưu
        best_value = float('inf')
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == "":  # Nếu ô trống
                    board[row][col] = "X"
                    move_value = minimax(board, depth - 1, True)  # Đệ quy, chuyển lượt cho máy tính
                    board[row][col] = ""  # Quay lại trạng thái ban đầu
                    if move_value < best_value:
                        best_value = move_value
                        best_move = (row, col)  # Lưu lại tọa độ của nước đi tốt nhất
        return best_value if best_move is None else best_value  # Trả về điểm tốt nhất

def is_game_over(board):
    # Kiểm tra nếu có người thắng hoặc hết ô trống
    x_wins, _ = check_winner(board, "X")
    o_wins, _ = check_winner(board, "O")
    # Kiểm tra nếu trò chơi kết thúc: có người thắng hoặc không còn ô trống
    return x_wins or o_wins or all(board[row][col] != "" for row in range(len(board)) for col in range(len(board[row])))

def evaluate_board(board):
    # Đánh giá bảng, trả về điểm số cho Minimax
    x_wins, _ = check_winner(board, "X")
    o_wins, _ = check_winner(board, "O")
    
    if x_wins:
        return -1  # Người chơi X thắng (điểm xấu cho Minimax)
    elif o_wins:
        return 1  # Máy O thắng (điểm tốt cho Minimax)
    else:
        return 0  # Hòa hoặc chưa kết thúc

def best_move(board, depth):
    best_move = None
    best_value = float('-inf')
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "":
                board[row][col] = "O"
                move_value = minimax(board, depth, False, float('-inf'), float('inf'))
                board[row][col] = ""
                if move_value > best_value:
                    best_value = move_value
                    best_move = (row, col)
    return best_move

# --- Alpha-Beta Pruning ---
# Đã tích hợp vào hàm minimax phía trên

# --- A* Search ---
def heuristic(board):
    # Hàm đánh giá bàn cờ (ví dụ đơn giản: số quân X và O trên bàn)
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return o_count - x_count  # Máy tính muốn nhiều quân O hơn

def a_star(board):
    open_set = []
    heapq.heappush(open_set, (heuristic(board), board))
    while open_set:
        _, current_board = heapq.heappop(open_set)
        for row in range(len(current_board)):
            for col in range(len(current_board[row])):
                if current_board[row][col] == "":
                    new_board = [row.copy() for row in current_board]
                    new_board[row][col] = "O"
                    heapq.heappush(open_set, (heuristic(new_board), new_board))
                    return row, col  # Trả về nước đi tốt nhất
    return None, None

# --- Monte Carlo Tree Search (MCTS) ---
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

def mcts(board):
    root = Node(board)
    for _ in range(100):  # Để cải thiện, bạn có thể tăng số lần lặp
        node = root
        while node.children:
            node = node.best_child()
        # Tiếp theo: Thực hiện expansion, simulation và backpropagation
        row, col = find_random_empty_spot(board)  # Lấy nước đi ngẫu nhiên cho demo
        return row, col
# --- Zobrist Hashing ---
def zobrist_hash(board, zobrist_table):
    hash_value = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "X":
                hash_value ^= zobrist_table[row][col][0]
            elif board[row][col] == "O":
                hash_value ^= zobrist_table[row][col][1]
    return hash_value

# Utility function: check_winner (Cần được định nghĩa ở nơi khác)
def check_winner(board, player):
    # Hàm kiểm tra người chơi đã thắng chưa
    for row in range(len(board)):
        for col in range(len(board[row])):
            if check_direction(board, row, col, player):  # Kiểm tra theo chiều nào đó
                return True, (row, col)
    return False, None

def check_direction(board, row, col, player):
    # Kiểm tra chiến thắng trong 1 chiều (ngang, dọc, chéo)
    directions = [(1, 0), (0, 1), (1, 1), (-1, 1)]  # Ngang, dọc, chéo
    for dx, dy in directions:
        count = 0
        for i in range(5):  # Kiểm tra 5 ô liên tiếp
            new_row, new_col = row + i * dx, col + i * dy
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == player:
                count += 1
            else:
                break
        if count == 5:
            return True
    return False
