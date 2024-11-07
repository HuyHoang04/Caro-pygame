# easy_ai.py

import math
from collections import defaultdict

class EasyAI:
    def __init__(self, gomoku, max_depth=2):
        self.gomoku = gomoku
        self.board = gomoku.board
        self.board_size = len(self.board)
        self.max_depth = max_depth
        self.memo = defaultdict(int)  # Memoization để lưu các trạng thái đã tính toán

    def make_move(self):
        best_score = -math.inf
        best_move = None

        # Chỉ kiểm tra các ô gần quân cờ hiện có
        potential_moves = self.get_potential_moves()

        for x, y in potential_moves:
            self.board[y][x] = "O"
            score = self.minimax(0, -math.inf, math.inf, False)
            self.board[y][x] = 0
            if score > best_score:
                best_score = score
                best_move = (x, y)

        if best_move:
            x, y = best_move
            self.gomoku.place_piece(x, y, "O")

    def get_potential_moves(self):
        """Lấy các nước đi khả thi xung quanh các quân cờ đã đặt"""
        moves = set()
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] != 0:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == 0:
                                moves.add((nx, ny))
        return list(moves)

    def minimax(self, depth, alpha, beta, is_maximizing):
        # Sử dụng memoization để tránh tính toán lại
        board_hash = self.hash_board()
        if board_hash in self.memo:
            return self.memo[board_hash]

        winner = self.check_winner()
        if winner == "O":
            return 10 - depth
        elif winner == "X":
            return depth - 10
        elif self.is_board_full() or depth == self.max_depth:
            return self.evaluate_board()

        if is_maximizing:
            max_eval = -math.inf
            for x, y in self.get_potential_moves():
                self.board[y][x] = "O"
                eval = self.minimax(depth + 1, alpha, beta, False)
                self.board[y][x] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.memo[board_hash] = max_eval  # Lưu giá trị tính toán
            return max_eval
        else:
            min_eval = math.inf
            for x, y in self.get_potential_moves():
                self.board[y][x] = "X"
                eval = self.minimax(depth + 1, alpha, beta, True)
                self.board[y][x] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.memo[board_hash] = min_eval  # Lưu giá trị tính toán
            return min_eval

    def check_winner(self):
        return self.gomoku.winner_checker.check_winner()

    def is_board_full(self):
        return all(self.board[y][x] != 0 for y in range(self.board_size) for x in range(self.board_size))

    def evaluate_board(self):
        """Đánh giá bàn cờ chỉ dựa trên các nước đi khả thi, giảm số vòng lặp"""
        score = 0
        potential_moves = self.get_potential_moves()
        for x, y in potential_moves:
            if self.board[y][x] == "O":
                score += self.evaluate_position(x, y, "O")
            elif self.board[y][x] == "X":
                score -= self.evaluate_position(x, y, "X")
        return score

    def evaluate_position(self, x, y, player):
        """Đánh giá điểm cho vị trí cụ thể mà không cần 3 vòng lặp"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0
        for dx, dy in directions:
            count, open_ends = 1, 0

            # Đếm số quân cờ liên tiếp theo hướng +dx, +dy
            for step in range(1, 5):
                nx, ny = x + step * dx, y + step * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == player:
                    count += 1
                else:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == 0:
                        open_ends += 1
                    break

            # Đếm số quân cờ liên tiếp theo hướng -dx, -dy
            for step in range(1, 5):
                nx, ny = x - step * dx, y - step * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == player:
                    count += 1
                else:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == 0:
                        open_ends += 1
                    break

            if count == 2 and open_ends == 2:
                score += 1
            elif count == 3 and open_ends == 2:
                score += 10
            elif count == 4 and open_ends == 2:
                score += 100
            elif count == 5:
                score += 1000
        return score

    def hash_board(self):
        """Tạo mã hash đơn giản cho bàn cờ hiện tại để dùng trong memoization"""
        return tuple(tuple(row) for row in self.board)
