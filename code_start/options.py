import pygame
import sys

pygame.init()

class Button:
    def __init__(self, text, pos, font, bg="black"):
        self.x, self.y = pos
        self.font = pygame.font.Font(font, 30)
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, True, pygame.Color("white"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False

def options_menu(screen):
    font = pygame.font.Font(None, 74)

    # Create option buttons
    choose_character_button = Button("Choose Character", (100, 100), None)
    settings_button = Button("Settings", (100, 200), None)
    back_button = Button("Back", (100, 300), None)

    selected_option = None

    while True:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.click(event):
                return

            if choose_character_button.click(event):
                selected_option = "Choose Character"
            if settings_button.click(event):
                selected_option = "Settings"

        choose_character_button.show(screen)
        settings_button.show(screen)
        back_button.show(screen)

        if selected_option == "Choose Character":
            display_choose_character(screen)
        elif selected_option == "Settings":
            display_settings(screen)

        pygame.display.flip()

def display_choose_character(screen):
    font = pygame.font.Font(None, 74)
    text = font.render('Choose Character Screen', True, pygame.Color('white'))
    screen.blit(text, (200, 400))

def display_settings(screen):
    font = pygame.font.Font(None, 74)
    text = font.render('Settings Screen', True, pygame.Color('white'))
    screen.blit(text, (200, 400))

def main_menu():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Main Menu')

    start_button = Button("Start", (350, 250), None)
    options_button = Button("Options", (350, 350), None)
    quit_button = Button("Quit", (350, 450), None)

    while True:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.click(event):
                print("Start Button Clicked")
                # Add functionality for start button

            if options_button.click(event):
                options_menu(screen)

            if quit_button.click(event):
                pygame.quit()
                sys.exit()

        start_button.show(screen)
        options_button.show(screen)
        quit_button.show(screen)

        pygame.display.flip()

main_menu()