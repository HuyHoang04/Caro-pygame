from game import Game
import pygame

def main():
    # Khởi tạo pygame
    pygame.init()
    
    try:
        # Tạo game và chạy
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Đảm bảo pygame được tắt đúng cách
        pygame.quit()

if __name__ == "__main__":
    main()