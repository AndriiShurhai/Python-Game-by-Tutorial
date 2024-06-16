from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pirates Adventures")
        self.clock = pygame.time.Clock()

        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)

        self.tmx_maps ={
            0: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', 'omni.tmx')),
            1: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', '0.tmx')),
            2: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', '1.tmx')),
            3: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', '2.tmx' )),
            4: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', '3.tmx')),
            5: load_pygame(join('..', 'Python Game Tutorial', 'data', 'levels', '4.tmx'))

        } 

        self.current_stage = Level(self.tmx_maps[5], self.level_frames, self.data)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'flag'),
            'saw': import_folder('..', 'Python Game Tutorial', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('..', 'Python Game Tutorial', 'graphics', 'enemies', 'saw', 'saw_chain'),
            'floor_spike': import_folder('..', 'Python Game Tutorial', 'graphics', 'enemies',  'floor_spikes'),
            'palms': import_sub_folders('..', 'Python Game Tutorial', 'graphics', 'level', 'palms'),
            'candle': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'candle'),
            'window': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'window'),
            'big_chain': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'small_chains'),
            'candle_light': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('..', 'Python Game Tutorial', 'graphics', 'player', 'Vasilko'),  # choosed_player_name
            'helicopter': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('..', 'Python Game Tutorial', 'graphics', 'objects', 'boat'),
            'spike': import_image('..', 'Python Game Tutorial', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('..', 'Python Game Tutorial', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('..', 'Python Game Tutorial', 'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('..', 'Python Game Tutorial', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('..', 'Python Game Tutorial', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('..', 'Python Game Tutorial', 'graphics', 'items'),
            'particle': import_folder('..', 'Python Game Tutorial', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('..', 'Python Game Tutorial', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('..', 'Python Game Tutorial', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('..', 'Python Game Tutorial', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('..', 'Python Game Tutorial', 'graphics', 'level', 'clouds', 'large_cloud')
        }

        self.font = pygame.font.Font(join('..', 'Python Game Tutorial', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('..', 'Python Game Tutorial', 'graphics', 'ui', 'heart'),
            'coin': import_image('..', 'Python Game Tutorial', 'graphics', 'ui', 'coin')
        }

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    sys.exit()
            self.current_stage.run(delta_time)
            self.ui.update(delta_time)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
