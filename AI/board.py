# from ast import Constant
from constants import Constant
class Board:
    def __init__(self):
        self.size = Constant.N
        self.win_condition = Constant.WIN_CONDITION
        self.board = [[0] * self.size for _ in range(self.size)]
        self.last_move = None
        
    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            self.last_move = (row, col)
            return True
        return False
    
    def has_winner(self):
        # Kiểm tra hàng ngang, dọc và đường chéo
        for i in range(Constant.N):
            for j in range(Constant.N):
                if self.board[i][j] != Constant.EMPTY:
                    if self.check_winner(i, j, self.board[i][j]):
                        return True
        return False
    
    def is_full(self):
        return all(cell != Constant.EMPTY for row in self.board for cell in row)
    
    def is_valid_move(self, row, col):
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == 0)

    def get_valid_moves(self):
        moves = []
        # Nếu là nước đi đầu tiên (chưa có last_move)
        if self.last_move is None:
            return [(self.size//2, self.size//2)]
            
        # Lấy các nước đi xung quanh nước đi cuối cùng trong phạm vi 2 ô
        for i in range(max(0, self.last_move[0]-2), 
                    min(self.size, self.last_move[0]+3)):
            for j in range(max(0, self.last_move[1]-2), 
                        min(self.size, self.last_move[1]+3)):
                if self.board[i][j] == Constant.EMPTY:
                    moves.append((i, j))

    # Nếu không có nước đi hợp lệ xung quanh, trả về tất cả các ô trống trên bàn cờ
        return moves if moves else [(i, j) for i in range(self.size) 
                                for j in range(self.size) 
                                if self.board[i][j] == Constant.EMPTY]

    def check_winner(self, row, col, player):
        # Kiểm tra hàng ngang
        count = 0
        for c in range(max(0, col - Constant.WIN_CONDITION + 1), min(Constant.N, col + Constant.WIN_CONDITION)):
            if self.board[row][c] == player:
                count += 1
                if count == Constant.WIN_CONDITION:
                    return True
            else:
                count = 0
                
        # Kiểm tra hàng dọc
        count = 0
        for r in range(max(0, row - Constant.WIN_CONDITION + 1), min(Constant.N, row + Constant.WIN_CONDITION)):
            if self.board[r][col] == player:
                count += 1
                if count == Constant.WIN_CONDITION:
                    return True
            else:
                count = 0
                
        # Kiểm tra đường chéo chính
        count = 0
        for i in range(-Constant.WIN_CONDITION + 1, Constant.WIN_CONDITION):
            r = row + i
            c = col + i
            if 0 <= r < Constant.N and 0 <= c < Constant.N:
                if self.board[r][c] == player:
                    count += 1
                    if count == Constant.WIN_CONDITION:
                        return True
                else:
                    count = 0
                    
        # Kiểm tra đường chéo phụ
        count = 0
        for i in range(-Constant.WIN_CONDITION + 1, Constant.WIN_CONDITION):
            r = row + i
            c = col - i
            if 0 <= r < Constant.N and 0 <= c < Constant.N:
                if self.board[r][c] == player:
                    count += 1
                    if count == Constant.WIN_CONDITION:
                        return True
                else:
                    count = 0
                    
        return False