import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

levels = ["EASY", "MEDIUM", "HARD"]
current_level_index = 0

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

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
    global current_level_index

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CARO GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 520), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        LEFT_ARROW = Button(image=pygame.image.load("assets/Left Arrow.png"), pos=(540, 400), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        
        RIGHT_ARROW = Button(image=pygame.image.load("assets/Right Arrow.png"), pos=(740, 400), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        LEVEL_TEXT = get_font(75).render(levels[current_level_index], True, "#d7fcd4")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 400))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, LEFT_ARROW, RIGHT_ARROW]:
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
                if LEFT_ARROW.checkForInput(MENU_MOUSE_POS):
                    current_level_index = (current_level_index - 1) % len(levels)
                if RIGHT_ARROW.checkForInput(MENU_MOUSE_POS):
                    current_level_index = (current_level_index + 1) % len(levels)

        pygame.display.update()

main_menu()
