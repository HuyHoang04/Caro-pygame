import random
from constants import N
from board import check_winner

def smart_move(board):
    # Kiểm tra xem máy có thể thắng ngay không
    for row in range(N):
        for col in range(N):
            if board[row][col] == '':
                board[row][col] = "O"
                if check_winner(board) == "O":
                    return row, col
                board[row][col] = ''  # Hoàn tác

    # Kiểm tra xem người chơi có thể thắng ở nước đi tiếp theo không
    for row in range(N):
        for col in range(N):
            if board[row][col] == '':
                board[row][col] = "X"
                if check_winner(board) == "X":
                    return row, col
                board[row][col] = ''  # Hoàn tác

    # Nếu không có nước đi thắng hay chặn, chọn một nước đi ngẫu nhiên
    while True:
        row = random.randint(0, N-1)
        col = random.randint(0, N-1)
        if board[row][col] == '':
            return row, col