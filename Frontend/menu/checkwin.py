# game_logic.py
from constants import *

def check_winner(board, symbol):
    size = get_board_size()
    win_condition = 5  # Số ký tự liên tiếp cần có để thắng
    
    # Kiểm tra các hàng
    for row in range(size):
        for col in range(size - win_condition + 1):
            if all(board[row][col + i] == symbol for i in range(win_condition)):
                return True

    # Kiểm tra các cột
    for col in range(size):
        for row in range(size - win_condition + 1):
            if all(board[row + i][col] == symbol for i in range(win_condition)):
                return True

    # Kiểm tra đường chéo chính (trái trên -> phải dưới)
    for row in range(size - win_condition + 1):
        for col in range(size - win_condition + 1):
            if all(board[row + i][col + i] == symbol for i in range(win_condition)):
                return True

    # Kiểm tra đường chéo phụ (phải trên -> trái dưới)
    for row in range(win_condition - 1, size):
        for col in range(size - win_condition + 1):
            if all(board[row - i][col + i] == symbol for i in range(win_condition)):
                return True

    # Không có ai thắng
    return False
