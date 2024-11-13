from constants import Constant
import random
from board import Board
import math
import time
from copy import deepcopy

class AI:
    def __init__(self, board, player, difficulty='medium', depth=None):
        self.depth_map = {
            'easy': 2,
            'medium': 3,
            'hard': 4
        }
        
        self.board = board
        self.player = player
        self.difficulty = difficulty
        self.depth = depth if depth is not None else self.depth_map[difficulty]
        
        self.algorithm_map = {
            'easy': 'minimax',
            'medium': 'alphabeta',
            'hard': 'mcts'
        }
        
        self.valid_moves_cache = {}
        self.evaluation_cache = {}
        
        self.WINNING_SCORE = 1000
        self.NEAR_WIN_SCORE = 100
        self.BLOCKING_SCORE = 80
    
    def is_terminal(self, board):
        """Kiểm tra xem trò chơi đã kết thúc chưa"""
        return board.is_full() or board.has_winner()

    def get_valid_moves(self, board):
        board_str = str(board.board)
        if board_str in self.valid_moves_cache:
            return self.valid_moves_cache[board_str]
        
        moves = [(i, j) 
                for i in range(Constant.N) 
                for j in range(Constant.N) 
                if board.board[i][j] == Constant.EMPTY]
        
        self.valid_moves_cache[board_str] = moves
        return moves

    def get_best_move(self):
        return getattr(self, f"{self.algorithm_map[self.difficulty]}_move")()

    def minimax_move(self):
        best_score = float('-inf')
        best_move = None
        depth = self.depth_map['easy']
        
        for move in self.get_valid_moves(self.board):
            row, col = move
            self.board.board[row][col] = self.player
            score = self.minimax(depth - 1, False)
            self.board.board[row][col] = Constant.EMPTY
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def minimax(self, depth, maximizing):
        if depth == 0 or self.is_terminal(self.board):
            return self.evaluate_board(self.board)

        score = float('-inf') if maximizing else float('inf')
        current_player = self.player if maximizing else -self.player
        
        for move in self.get_valid_moves(self.board):
            row, col = move
            self.board.board[row][col] = current_player
            eval_score = self.minimax(depth - 1, not maximizing)
            self.board.board[row][col] = Constant.EMPTY
            
            score = max(score, eval_score) if maximizing else min(score, eval_score)
            
        return score

    def alphabeta_move(self):
        depth = self.depth_map['medium']
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.get_valid_moves(self.board):
            row, col = move
            self.board.board[row][col] = self.player
            score = self.alphabeta(depth - 1, alpha, beta, False)
            self.board.board[row][col] = Constant.EMPTY
            
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            
        return best_move

    def alphabeta(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_terminal(self.board):
            return self.evaluate_board(self.board)

        current_player = self.player if maximizing else -self.player
        
        for move in self.get_valid_moves(self.board):
            row, col = move
            self.board.board[row][col] = current_player
            score = self.alphabeta(depth - 1, alpha, beta, not maximizing)
            self.board.board[row][col] = Constant.EMPTY
            
            if maximizing:
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            else:
                beta = min(beta, score)
                if beta <= alpha:
                    break
                
        return alpha if maximizing else beta

    def mcts_move(self):
        class Node:
            def __init__(self, state, parent=None):
                self.state = state
                self.parent = parent
                self.children = []
                self.visits = 0
                self.value = 0

        def uct_value(node, parent_visits, c=1.41):
            if node.visits == 0:
                return float('inf')
            return (node.value / node.visits) + c * math.sqrt(math.log(parent_visits) / node.visits)

        def select(node):
            while node.children and not self.is_terminal(node.state):
                node = max(node.children, key=lambda x: uct_value(x, node.visits))
            return node

        def expand(node):
            if self.is_terminal(node.state):
                return node
                
            moves = self.get_valid_moves(node.state)
            if not moves:
                return node

            for move in moves:
                row, col = move
                new_state = Board(node.state.size)  # Tạo bảng mới với kích thước tương tự
                new_state.board = [row[:] for row in node.state.board]  # Copy trạng thái bảng
                new_state.make_move(row, col, self.player)
                child = Node(new_state, node)
                node.children.append(child)
            
            return random.choice(node.children)

        def simulate(state):
            current_state = Board(state.size)
            current_state.board = [row[:] for row in state.board]
            current_player = self.player
            
            while not self.is_terminal(current_state):
                moves = self.get_valid_moves(current_state)
                if not moves:
                    break
                row, col = random.choice(moves)
                current_state.make_move(row, col, current_player)
                current_player = -current_player
                
            return self.evaluate_board(current_state)

        def backpropagate(node, result):
            while node:
                node.visits += 1
                node.value += result
                node = node.parent

        root = Node(self.board)
        iterations = 1000
        time_limit = 1.0
        start_time = time.time()
        
        for _ in range(iterations):
            if time.time() - start_time > time_limit:
                break
                
            leaf = select(root)
            child = expand(leaf)
            result = simulate(child.state)
            backpropagate(child, result)

        if not root.children:
            return None
            
        best_child = max(root.children, key=lambda x: x.visits)
        
        # Tìm nước đi dẫn đến trạng thái tốt nhất
        for row in range(Constant.N):
            for col in range(Constant.N):
                if self.board.board[row][col] != best_child.state.board[row][col]:
                    return (row, col)
        return None

    def evaluate_board(self, board):
        board_str = str(board.board)
        if board_str in self.evaluation_cache:
            return self.evaluation_cache[board_str]
            
        score = 0
        directions = [
            # Horizontal
            [(0, i) for i in range(Constant.WIN_CONDITION)],
            # Vertical
            [(i, 0) for i in range(Constant.WIN_CONDITION)],
            # Diagonal
            [(i, i) for i in range(Constant.WIN_CONDITION)],
            # Anti-diagonal
            [(i, Constant.WIN_CONDITION-1-i) for i in range(Constant.WIN_CONDITION)]
        ]

        for i in range(Constant.N - Constant.WIN_CONDITION + 1):
            for j in range(Constant.N - Constant.WIN_CONDITION + 1):
                for direction in directions:
                    window = [board.board[i + di][j + dj] for di, dj in direction 
                             if 0 <= i + di < Constant.N and 0 <= j + dj < Constant.N]
                    
                    if len(window) == Constant.WIN_CONDITION:
                        score += self.evaluate_window(window)

        self.evaluation_cache[board_str] = score
        return score

    def evaluate_window(self, window):
        player_count = window.count(self.player)
        opponent_count = window.count(-self.player)
        empty_count = window.count(Constant.EMPTY)

        if player_count == Constant.WIN_CONDITION:
            return self.WINNING_SCORE
        if opponent_count == Constant.WIN_CONDITION:
            return -self.WINNING_SCORE
            
        score = 0
        if player_count == Constant.WIN_CONDITION - 1 and empty_count == 1:
            score += self.NEAR_WIN_SCORE
        if opponent_count == Constant.WIN_CONDITION - 1 and empty_count == 1:
            score -= self.BLOCKING_SCORE
            
        return score