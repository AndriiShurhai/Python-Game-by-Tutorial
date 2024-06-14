from settings import *
from sprites import Heart
from manual_timer import Timer

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        # health
        self.heart_frames = frames['heart']
        self.heart_surface_width = self.heart_frames[0].get_width()
        self.heart_spacing = 5

        # coins
        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surface = frames['coin']

    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(amount):
            y = 10
            x = 10 + heart * (self.heart_surface_width + self.heart_spacing)
            Heart((x, y), self.heart_frames, self.sprites)
    
    def display_text(self):
        if self.coin_timer.active:
            text_surface = self.font.render(str(self.coin_amount), False, 'white')
            text_rect = text_surface.get_frect(topleft=(16,34)).move(30,0)

            self.display_surface.blit(text_surface, text_rect)

            coin_rect = self.coin_surface.get_frect(center=text_rect.bottomleft).move(-20, -20)
            self.display_surface.blit(self.coin_surface, coin_rect) 

    def show_coins(self, amount):
        self.coin_amount = amount
        self.coin_timer.activate()

    def update(self, delta_time):
        self.coin_timer.update()
        self.sprites.update(delta_time)
        self.sprites.draw(self.display_surface)
        self.display_text()