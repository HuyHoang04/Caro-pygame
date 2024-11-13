import pygame
from constants import Constant

class Graphics:
    def draw_board(self, board, screen):
        # Vẽ khung
        pygame.draw.rect(screen, Constant.FRAME_COLOR,
                        (Constant.GRID_OFFSET_X - Constant.FRAME_WIDTH, 
                         Constant.GRID_OFFSET_Y - Constant.FRAME_WIDTH,
                         Constant.N * Constant.CELL_SIZE + 2 * Constant.FRAME_WIDTH, 
                         Constant.N * Constant.CELL_SIZE + 2 * Constant.FRAME_WIDTH))
        
        # Vẽ nền lưới
        pygame.draw.rect(screen, Constant.BLUE,
                        (Constant.GRID_OFFSET_X, Constant.GRID_OFFSET_Y, 
                         Constant.N * Constant.CELL_SIZE, Constant.N * Constant.CELL_SIZE))
        
        # Vẽ lưới
        for i in range(Constant.N + 1):
            # Đường dọc
            pygame.draw.line(screen, Constant.BLACK,
                           (Constant.GRID_OFFSET_X + i * Constant.CELL_SIZE, Constant.GRID_OFFSET_Y),
                           (Constant.GRID_OFFSET_X + i * Constant.CELL_SIZE, 
                            Constant.GRID_OFFSET_Y + Constant.N * Constant.CELL_SIZE))
            # Đường ngang
            pygame.draw.line(screen, Constant.BLACK,
                           (Constant.GRID_OFFSET_X, Constant.GRID_OFFSET_Y + i * Constant.CELL_SIZE),
                           (Constant.GRID_OFFSET_X + Constant.N * Constant.CELL_SIZE, 
                            Constant.GRID_OFFSET_Y + i * Constant.CELL_SIZE))
        
        # Vẽ X và O
        for i in range(Constant.N):
            for j in range(Constant.N):
                if board.board[i][j] == 1:
                    self.draw_x(i, j, screen)
                elif board.board[i][j] == -1:
                    self.draw_o(i, j, screen)
    
    def draw_x(self, row, col, screen):
        x = Constant.GRID_OFFSET_X + col * Constant.CELL_SIZE
        y = Constant.GRID_OFFSET_Y + row * Constant.CELL_SIZE
        margin = 5
        pygame.draw.line(screen, Constant.RED,
                        (x + margin, y + margin),
                        (x + Constant.CELL_SIZE - margin, 
                         y + Constant.CELL_SIZE - margin), 
                        Constant.LINE_WIDTH)
        pygame.draw.line(screen, Constant.RED,
                        (x + Constant.CELL_SIZE - margin, y + margin),
                        (x + margin, y + Constant.CELL_SIZE - margin), 
                        Constant.LINE_WIDTH)
    
    def draw_o(self, row, col, screen):
        x = Constant.GRID_OFFSET_X + col * Constant.CELL_SIZE + Constant.CELL_SIZE // 2
        y = Constant.GRID_OFFSET_Y + row * Constant.CELL_SIZE + Constant.CELL_SIZE // 2
        margin = 5
        pygame.draw.circle(screen, Constant.BLACK,
                         (x, y), 
                         (Constant.CELL_SIZE - 2 * margin) // 2, 
                         Constant.LINE_WIDTH)