# game_logic.py
from constants import *

def check_winner(board, symbol):
    size = get_board_size()
    win_length = 5  # Số ký tự liên tiếp cần có để thắng
    
    # Kiểm tra theo hàng ngang
    for row in range(size):
        for col in range(size - win_length + 1):
            if all(board[row][col + i] == symbol for i in range(win_length)):
                return True, [(row, col + i) for i in range(win_length)]

    # Kiểm tra theo hàng dọc
    for col in range(size):
        for row in range(size - win_length + 1):
            if all(board[row + i][col] == symbol for i in range(win_length)):
                return True, [(row + i, col) for i in range(win_length)]

    # Kiểm tra đường chéo chính (trái trên xuống phải dưới)
    for row in range(size - win_length + 1):
        for col in range(size - win_length + 1):
            if all(board[row + i][col + i] == symbol for i in range(win_length)):
                return True, [(row + i, col + i) for i in range(win_length)]

    # Kiểm tra đường chéo phụ (phải trên xuống trái dưới)
    for row in range(win_length - 1, size):
        for col in range(size - win_length + 1):
            if all(board[row - i][col + i] == symbol for i in range(win_length)):
                return True, [(row - i, col + i) for i in range(win_length)]

    return False, []  # Không tìm thấy người thắng

