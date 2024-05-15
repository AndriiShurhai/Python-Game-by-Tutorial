from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pirates Adventures")
        self.clock = pygame.time.Clock()

        self.tmx_maps ={
            0: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', 'omni.tmx'))
        }

        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    sys.exit()
            self.current_stage.run(delta_time)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
