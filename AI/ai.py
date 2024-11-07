# ai.py

import random

class AIMove:
    def __init__(self, gomoku):
        self.gomoku = gomoku

    def make_move(self):
        for y in range(15):
            for x in range(15):
                if self.gomoku.board[y][x] is None:
                    self.gomoku.board[y][x] = self.gomoku.current_turn
                    self.gomoku.switch_turn()
                    return
