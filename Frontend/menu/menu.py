import pygame, sys
from button import Button
from constants import *
from graphics import draw_grid, draw_symbols

pygame.init()

SCREEN = pygame.display.set_mode((1280, 920))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background2.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

levels = ["EASY", "MEDIUM", "HARD"]
current_level_index = 0

board_sizes = ["3x3", "10x10", "15x15", "18x18"]
current_size_index = 2  # Default to 15x15

def play():
    board_size = int(board_sizes[current_size_index].split('x')[0])
    global N
    N = board_size
    update_grid_offset()

    board = [["" for _ in range(N)] for _ in range(N)]

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        draw_grid(SCREEN)
        draw_symbols(SCREEN, board)

        PLAY_BACK = Button(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    global current_level_index, current_size_index

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CARO GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 480), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        LEFT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 250), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_LEVEL = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 250), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        LEVEL_TEXT = get_font(35).render(levels[current_level_index], True, "#d7fcd4")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 250))

        LEFT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-left2.png"), pos=(440, 350), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW_SIZE = Button(image=pygame.image.load("assets/arrow-right2.png"), pos=(840, 350), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        SIZE_TEXT = get_font(35).render(board_sizes[current_size_index], True, "#d7fcd4")
        SIZE_RECT = SIZE_TEXT.get_rect(center=(640, 350))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
        SCREEN.blit(SIZE_TEXT, SIZE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, LEFT_ARROW_LEVEL, RIGHT_ARROW_LEVEL, LEFT_ARROW_SIZE, RIGHT_ARROW_SIZE]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if LEFT_ARROW_LEVEL.checkForInput(MENU_MOUSE_POS):
                    current_level_index = (current_level_index - 1) % len(levels)
                if RIGHT_ARROW_LEVEL.checkForInput(MENU_MOUSE_POS):
                    current_level_index = (current_level_index + 1) % len(levels)
                if LEFT_ARROW_SIZE.checkForInput(MENU_MOUSE_POS):
                    current_size_index = (current_size_index - 1) % len(board_sizes)
                if RIGHT_ARROW_SIZE.checkForInput(MENU_MOUSE_POS):
                    current_size_index = (current_size_index + 1) % len(board_sizes)

        pygame.display.update()

main_menu()
