# main.py

import pygame
import sys
from gomoku import Gomoku
from player import PlayerMove
from ai import AIMove
from winner import WinnerChecker

# Khởi tạo pygame và cấu hình
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Gomoku Game")

# Khởi tạo trò chơi và các đối tượng người chơi và AI
gomoku = Gomoku()
player = PlayerMove(gomoku)
ai = AIMove(gomoku)
winner_checker = WinnerChecker(gomoku)

# Thêm cờ để kiểm tra người thắng
winner = None

# Vòng lặp chính của trò chơi
def main():
    global winner
    while True:
        screen.fill((255, 255, 255))
        gomoku.draw_board(screen)
        gomoku.draw_pieces(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and gomoku.current_turn == "X" and not winner:
                player.handle_click(pygame.mouse.get_pos())
            elif gomoku.current_turn == "O" and not winner:
                ai.make_move()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                gomoku.reset_game()
                winner = None  # Reset lại trạng thái người thắng
                winner_checker.winning_coords = None  # Xóa tọa độ chiến thắng

        # Kiểm tra người thắng nếu chưa có ai thắng
        if not winner:
            winner = winner_checker.check_winner()
            if winner:
                print(f"Người thắng: {winner}")
                print(f"Vị trí nước đi chiến thắng cuối cùng: {winner_checker.winning_coords}")
                # Đánh dấu ô chiến thắng cuối cùng trên màn hình
                if winner_checker.winning_coords:
                    x, y = winner_checker.winning_coords
                    pygame.draw.circle(screen, (0, 255, 0), 
                                       (x * (600 // 15) + (600 // 15) // 2, 
                                        y * (600 // 15) + (600 // 15) // 2), 10)

        pygame.display.flip()

# Chạy trò chơi
if __name__ == "__main__":
    main()
