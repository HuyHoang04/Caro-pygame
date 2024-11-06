import pygame
import random
from checkwin import check_winner
from constants import get_board_size

def minimax(board, depth, is_maximizing, alpha, beta):
    winner, _ = check_winner(board, "X")
    if winner:
        return -1  # Người chơi thắng -> AI thua
    winner, _ = check_winner(board, "O")
    if winner:
        return 1  # AI thắng
    if depth == 0 or all(board[row][col] != "" for row in range(get_board_size()) for col in range(get_board_size())):
        return 0  # Hòa hoặc hết lượt

    if is_maximizing:  # AI's turn (maximize score)
        max_eval = float('-inf')
        for row in range(get_board_size()):
            for col in range(get_board_size()):
                if board[row][col] == "":
                    board[row][col] = "O"  # AI đánh
                    eval = minimax(board, depth - 1, False, alpha, beta)
                    board[row][col] = ""  # Quay lại trạng thái ban đầu
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Cắt tỉa beta
        return max_eval
    else:  # Player's turn (minimize score)
        min_eval = float('inf')
        for row in range(get_board_size()):
            for col in range(get_board_size()):
                if board[row][col] == "":
                    board[row][col] = "X"  # Người chơi đánh
                    eval = minimax(board, depth - 1, True, alpha, beta)
                    board[row][col] = ""  # Quay lại trạng thái ban đầu
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Cắt tỉa alpha
        return min_eval

def find_best_move(board):
    best_score = float('-inf')
    best_move = None
    for row in range(get_board_size()):
        for col in range(get_board_size()):
            if board[row][col] == "":
                board[row][col] = "O"  # AI đánh
                score = minimax(board, 3, False, float('-inf'), float('inf'))  # Độ sâu có thể thay đổi
                board[row][col] = ""  # Quay lại trạng thái ban đầu
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move