# winner.py

class WinnerChecker:
    def __init__(self, gomoku):
        self.gomoku = gomoku
        self.board = gomoku.board
        self.board_size = len(self.board)
        self.win_condition = 5
        self.winning_coords = None  # Lưu tọa độ nước đi chiến thắng

    def check_winner(self):
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x]:
                    if (self.check_direction(x, y, 1, 0) or
                        self.check_direction(x, y, 0, 1) or
                        self.check_direction(x, y, 1, 1) or
                        self.check_direction(x, y, 1, -1)):
                        return self.board[y][x]  # Trả về người thắng (X hoặc O)
        return None

    def check_direction(self, x, y, dx, dy):
        """
        Kiểm tra một hướng cho chuỗi 5 quân liên tiếp.
        Nếu thắng, lưu tọa độ của quân thứ 5 trong `self.winning_coords`.
        """
        target = self.board[y][x]
        count = 0
        for i in range(self.win_condition):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size and self.board[ny][nx] == target:
                count += 1
            else:
                break
        if count == self.win_condition:
            # Lưu tọa độ quân cờ chiến thắng cuối cùng
            self.winning_coords = (nx - dx, ny - dy)
            return True
        return False
