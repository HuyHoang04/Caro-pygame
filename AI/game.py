import pygame
from constants import Constant
from board import Board
from graphics import Graphics
from ai import AI

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((Constant.WIDTH, Constant.HEIGHT))
        pygame.display.set_caption("Caro Game")
        self.game_mode = None
        self.board = None
        self.graphics = None
        self.ai = None
        self.current_player = None
        self.game_over = None
        
    def show_menu(self):
    # Khởi tạo font
        menu_font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 74)
        
        # Tạo text cho menu chính
        title_text = title_font.render("CARO GAME", True, Constant.BLACK)
        pvp_text = menu_font.render("Press 1: Player vs Player", True, Constant.BLACK)
        pve_text = menu_font.render("Press 2: Player vs Computer", True, Constant.BLACK)
        quit_text = menu_font.render("Press Q: Quit Game", True, Constant.BLACK)
        
        # Menu state để theo dõi trạng thái hiện tại
        current_menu = "main"  # Có thể là "main" hoặc "difficulty"
        
        # Text cho menu độ khó
        diff_title_text = title_font.render("Select Difficulty", True, Constant.BLACK)
        easy_text = menu_font.render("Press 1: Easy", True, Constant.BLACK)
        medium_text = menu_font.render("Press 2: Medium", True, Constant.BLACK)
        hard_text = menu_font.render("Press 3: Hard", True, Constant.BLACK)
        back_text = menu_font.render("Press B: Back", True, Constant.BLACK)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.KEYDOWN:
                    if current_menu == "main":
                        if event.key == pygame.K_1:
                            return "PvP"
                        elif event.key == pygame.K_2:
                            current_menu = "difficulty"
                        elif event.key == pygame.K_q:
                            return "QUIT"
                    
                    elif current_menu == "difficulty":
                        if event.key == pygame.K_1:
                            return ("PvE", "easy")
                        elif event.key == pygame.K_2:
                            return ("PvE", "medium")
                        elif event.key == pygame.K_3:
                            return ("PvE", "hard")
                        elif event.key == pygame.K_b:
                            current_menu = "main"
            
            # Xóa màn hình
            self.screen.fill(Constant.BACKGROUND_COLOR)
            
            if current_menu == "main":
                # Vẽ menu chính
                title_rect = title_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//4))
                pvp_rect = pvp_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2))
                pve_rect = pve_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2 + 50))
                quit_rect = quit_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2 + 100))
                
                self.screen.blit(title_text, title_rect)
                self.screen.blit(pvp_text, pvp_rect)
                self.screen.blit(pve_text, pve_rect)
                self.screen.blit(quit_text, quit_rect)
                
            elif current_menu == "difficulty":
                # Vẽ menu độ khó
                title_rect = diff_title_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//4))
                easy_rect = easy_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2))
                medium_rect = medium_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2 + 50))
                hard_rect = hard_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2 + 100))
                back_rect = back_text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT//2 + 150))
                
                self.screen.blit(diff_title_text, title_rect)
                self.screen.blit(easy_text, easy_rect)
                self.screen.blit(medium_text, medium_rect)
                self.screen.blit(hard_text, hard_rect)
                self.screen.blit(back_text, back_rect)
            
            pygame.display.flip()

    def initialize_game(self, game_mode, difficulty=None):
        self.board = Board()
        self.graphics = Graphics()
        self.game_mode = game_mode
        self.current_player = 1
        self.game_over = False
        
        if game_mode == "PvE":
            # Điều chỉnh độ khó của AI
            if difficulty == "easy":
                self.ai = AI(self.board, -1, depth=1)
            elif difficulty == "medium":
                self.ai = AI(self.board, -1, depth=2)
            elif difficulty == "hard":
                self.ai = AI(self.board, -1, depth=3)
            else:
                self.ai = AI(self.board, -1, depth=2)  # Default to medium if no difficulty specified
    def ai_move(self):
            if self.ai:
                row, col = self.ai.get_best_move()
                if self.board.make_move(row, col, -1):  # -1 là giá trị cho AI
                    if self.board.check_winner(row, col, -1):
                        self.game_over = True
                        print("Computer wins!")
                    elif self.board.is_full():
                        self.game_over = True
                        print("Game Draw!")
                    else:
                        self.current_player = 1 
                        
    def handle_click(self, pos):
        if self.game_over or (self.game_mode == "PvE" and self.current_player == -1):
            return
            
        grid_x = pos[0] - Constant.GRID_OFFSET_X
        grid_y = pos[1] - Constant.GRID_OFFSET_Y
        
        if (0 <= grid_x <= Constant.N * Constant.CELL_SIZE and 
            0 <= grid_y <= Constant.N * Constant.CELL_SIZE):
            col = grid_x // Constant.CELL_SIZE
            row = grid_y // Constant.CELL_SIZE
            
            if self.board.make_move(row, col, self.current_player):
                if self.board.check_winner(row, col, self.current_player):
                    self.game_over = True
                    winner = "Player 1" if self.current_player == 1 else "Player 2"
                    if self.game_mode == "PvE" and self.current_player == -1:
                        winner = "Computer"
                    print(f"{winner} wins!")
                elif self.board.is_full():  # Thêm kiểm tra hòa
                    self.game_over = True
                    print("Game Draw!")
                else:
                    self.current_player = -self.current_player
                    if self.game_mode == "PvE" and self.current_player == -1:
                        self.ai_move()

    def run(self):
        while True:
            # Hiện menu và lấy lựa chọn
            menu_choice = self.show_menu()
            
            # Xử lý lựa chọn từ menu
            if menu_choice == "QUIT":
                break
            elif menu_choice == "PvP":
                self.initialize_game("PvP")
            elif isinstance(menu_choice, tuple) and menu_choice[0] == "PvE":
                self.initialize_game("PvE", menu_choice[1])  # Truyền cả game mode và độ khó
            else:
                continue
            
            # Game loop
            clock = pygame.time.Clock()
            running = True
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return  # Thoát hoàn toàn khỏi game
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.handle_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Reset game
                            running = False
                        elif event.key == pygame.K_q:  # Quit to menu
                            running = False
                
                # Vẽ game
                self.screen.fill(Constant.BACKGROUND_COLOR)
                self.graphics.draw_board(self.board, self.screen)
                
                # Hiển thị thông báo khi game kết thúc
                if self.game_over:
                    font = pygame.font.Font(None, 36)
                    if self.board.is_full() and not self.board.has_winner():
                        text = font.render("Game Draw! Press R to restart or Q to quit", True, Constant.BLACK)
                    else:
                        winner = "Player 1" if self.current_player == 1 else "Player 2"
                        if self.game_mode == "PvE" and self.current_player == -1:
                            winner = "Computer"
                        text = font.render(f"{winner} wins! Press R to restart or Q to quit", True, Constant.BLACK)
                    text_rect = text.get_rect(center=(Constant.WIDTH//2, Constant.HEIGHT - 50))
                    self.screen.blit(text, text_rect)
                
                # Hiển thị lượt chơi hiện tại
                if not self.game_over:
                    font = pygame.font.Font(None, 36)
                    current = "Player 1" if self.current_player == 1 else ("Computer" if self.game_mode == "PvE" else "Player 2")
                    turn_text = font.render(f"Current Turn: {current}", True, Constant.BLACK)
                    turn_rect = turn_text.get_rect(center=(Constant.WIDTH//2, 30))
                    self.screen.blit(turn_text, turn_rect)
                
                pygame.display.flip()
                clock.tick(60)
    
    
        