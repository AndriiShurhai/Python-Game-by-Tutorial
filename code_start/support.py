from settings import *
from os import walk
from os.path import join

# import a single frame
def import_image(*path, alpha=True, format='png'):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

# import all frames in the folder in list
def import_folder(*path):
    frames = []
    for folder_path, subfolders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
            print(image_name)
            full_path = join(folder_path, image_name)
            print(full_path)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames 

# import all frames in the folder in dictionary with lists
def import_folder_dict(*path):
    frame_dict = {}
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frame_dict[image_name.split('.')[0]] = surface
    return frame_dict

# import starting with parent folders
def import_sub_folders(*path):
    frame_dict = {}
    for _, sub_folders, __ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict
