import pygame
from button import Button
from support import *
from settings import *
from game_play import game
from options import options


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # images
        self.background = import_image(join('..', 'Python Game Tutorial', 'graphics', 'menu', 'main_menu', 'Background'))
        self.play_image = import_image(join('..', 'Python Game Tutorial', 'graphics', 'menu', 'main_menu', 'Play Rect'))
        self.options_image = import_image(join('..', 'Python Game Tutorial', 'graphics', 'menu', 'main_menu', 'Options Rect'))
        self.quit_image = import_image(join('..', 'Python Game Tutorial', 'graphics', 'menu', 'main_menu', 'Quit Rect'))


        # buttons
        self.play_button = Button(
            image=self.play_image, 
            pos=(640, 250), 
            text_input="PLAY", 
            font=self.get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
            ) 

        self.options_button = Button(
            image=self.options_image,
            pos=(640, 400), 
            text_input="OPTIONS", 
            font=self.get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
         )
        
        self.quit_button = Button(
            image=self.quit_image,
            pos=(640, 550), 
            text_input="QUIT", 
            font=self.get_font(75), 
            base_color="#d7fcd4", 
            hovering_color="White"
        )

    def get_font(self, size):
        return pygame.font.Font(join('..', 'Python Game Tutorial', 'graphics', 'menu', 'main_menu', 'font.ttf'), size)

    def run(self):
        pygame.display.set_caption('main menu')

        while True:
            self.screen.blit(self.background, (0, 0))
            menu_mouse_position = pygame.mouse.get_pos()
            menu_text = self.get_font(70).render('Pirates Adventure', True, '#b68f40')
            menu_rect = menu_text.get_frect(center=(640,100))
            
            self.screen.blit(menu_text, menu_rect)

            for button in [self.play_button, self.options_button, self.quit_button]:
                button.changeColor(menu_mouse_position)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkForInput(menu_mouse_position):
                        game.run()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.options_button.checkForInput(menu_mouse_position):
                        options(WINDOW_WIDTH, WINDOW_HEIGHT)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.quit_button.checkForInput(menu_mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


main_menu = MainMenu()

main_menu.run()