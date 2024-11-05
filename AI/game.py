import pygame
from constants import *
from board import create_board, check_winner, is_full
from ai import smart_move
from graphics import draw_grid, draw_symbols

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cờ Caro 15x15 với AI")
        self.board = create_board()
        self.current_player = "X"

    def player_move(self, row, col):
        if self.board[row][col] == '' and not check_winner(self.board):
            self.board[row][col] = self.current_player
            if check_winner(self.board) or is_full(self.board):
                return
            self.current_player = "O" if self.current_player == "X" else "X"
            if self.current_player == "O":
                ai_row, ai_col = smart_move(self.board)
                self.board[ai_row][ai_col] = "O"
                self.current_player = "X"

    def run(self):
        draw_grid(self.screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.current_player == "X":
                    x, y = event.pos
                    row, col = (y - GRID_OFFSET_Y) // CELL_SIZE, (x - GRID_OFFSET_X) // CELL_SIZE
                    if 0 <= row < N and 0 <= col < N:
                        self.player_move(row, col)
                        draw_symbols(self.screen, self.board)
                        winner = check_winner(self.board)
                        if winner:
                            print(f"{winner} thắng!")
                            pygame.time.wait(2000)
                            self.board = create_board()
                            draw_grid(self.screen)
                            draw_symbols(self.screen, self.board)

            draw_symbols(self.screen, self.board)
            pygame.display.update()

        pygame.quit()
        pygame.display.update()