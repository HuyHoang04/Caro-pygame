# player.py

class PlayerMove:
    def __init__(self, gomoku):
        self.gomoku = gomoku

    def handle_click(self, pos):
        x, y = pos[0] // (600 // 15), pos[1] // (600 // 15)  # Tính toán vị trí trên bàn cờ
        if self.gomoku.board[y][x] is None:
            self.gomoku.board[y][x] = self.gomoku.current_turn
            self.gomoku.switch_turn()
