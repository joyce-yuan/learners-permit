import pygame
import sys
import pygame_menu
from os import listdir
from pygame_menu.examples import create_example_window


surface = create_example_window('Example - Simple', (900, 600))

menu = pygame_menu.Menu(
        height=300,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Choose Data Set',
        width=400
    )

path_to_dir = './'
all_files = listdir(path_to_dir)
csv_files = [ filename for filename in all_files if filename.endswith(".csv")]


for index, filename in enumerate(csv_files):
    menu.add.button(f'File {index}', print, filename)


if __name__ == '__main__':
    while True:
        menu.mainloop(surface)