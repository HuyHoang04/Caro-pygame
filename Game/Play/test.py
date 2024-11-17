import pygame
import random
from checkwin import check_winner
from constants import get_board_size

# test.py
from constants import *

# Hàm tính điểm của mỗi nước đi
def evaluate(board):
    # Kiểm tra xem ai có thắng không
    if check_winner(board, "O")[0]:
        return 1  # AI thắng
    elif check_winner(board, "X")[0]:
        return -1  # Người chơi thắng
    return 0  # Không có ai thắng

# Hàm Minimax
def minimax(board, depth, is_maximizing_player):
    score = evaluate(board)

    # Nếu đã thắng hoặc thua, trả về điểm
    if score == 1 or score == -1:
        return score

    # Nếu bàn cờ đầy, hòa
    if not any("" in row for row in board):
        return 0

    if is_maximizing_player:
        best = -float('inf')  # AI tìm kiếm để tối đa hóa điểm
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == "":
                    board[row][col] = "O"  # AI đánh O
                    best = max(best, minimax(board, depth + 1, False))
                    board[row][col] = ""  # Quay lại bước trước
        return best
    else:
        best = float('inf')  # Người chơi tìm kiếm để tối thiểu hóa điểm
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == "":
                    board[row][col] = "X"  # Người chơi đánh X
                    best = min(best, minimax(board, depth + 1, True))
                    board[row][col] = ""  # Quay lại bước trước
        return best

# Hàm tìm nước đi tốt nhất
def find_best_move(board, level="EASY"):
    best_val = -float('inf')
    best_move = (-1, -1)

    # Cấu hình độ sâu cho AI dựa trên mức độ khó
    if level == "EASY":
        depth = 1
    elif level == "MEDIUM":
        depth = 3
    else:
        depth = 5  # Độ khó HARD sẽ sử dụng độ sâu lớn hơn

    # Thử tất cả các nước đi và tính điểm để chọn nước đi tốt nhất
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "":
                board[row][col] = "O"  # AI đánh O
                move_val = minimax(board, 0, False)
                board[row][col] = ""  # Quay lại bước trước

                if move_val > best_val:
                    best_move = (row, col)
                    best_val = move_val

    return best_move
