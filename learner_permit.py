import pygame
import sys
import pygame_menu
from pygame_menu.examples import create_example_window
from car_game import CarGame as GameMode
from car_game_playback_mode import CarGame as PlaybackMode
from car_game_generate_mode import CarGame as GenerateMode
from os import listdir


### Trial 2 from https://pygame-menu.readthedocs.io/en/4.2.8/

from typing import Tuple, Any

surface = create_example_window('Example - Simple', (900, 600))


def set_difficulty(selected: Tuple, value: Any) -> None:
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')


def start_the_game() -> None:
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.
    """
    global user_name
    print(f'{user_name.get_value()}, Do the job here!')


def game_mode() -> None:
    """
    Function that runs the game in game mode
    Allows user to control the car through arrow keys
    """

    print("Game mode running")
    play(GameMode())

def inspect_data() -> None:
    """
    takes in a csv file as data
    steps through each of the data points
    """
    # def find_csv_filenames( path_to_dir, suffix=".csv" ):
    #     filenames = listdir(path_to_dir)
    #     return [ filename for filename in filenames if filename.endswith( suffix ) ]
    
    # find csv filename

    path_to_dir = './data/'
    all_files = listdir(path_to_dir)
    csv_files = [ filename for filename in all_files if filename.endswith(".csv")]

    print("Inspect / Playback data")
    data_menu = pygame_menu.Menu(
        height=300,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Choose Data Set',
        width=400
    )

    global input_file
    input_file = ''

    def set_data(filename):
        global input_file
        input_file = filename
        print(input_file)

    for index, filename in enumerate(csv_files):
        data_menu.add.button(filename, set_data, filename)

    # chooseDataMenu.draw(surface)

    while input_file == '':
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        data_menu.update(events)
        data_menu.draw(surface)
        pygame.display.update()

    play(PlaybackMode(path_to_dir + input_file))

def generate_data() -> None:
    """
    user can play with the playground screen to drag and drop cars
    then the car game runs and shows the outcome
    """

    print("Generate data")

    global loop
    loop = True
    def end_loop():
        global loop
        loop = False

    input_menu = pygame_menu.Menu(
        height=300,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Create Clip Name',
        width=400
    )

    clip_name = input_menu.add.text_input('', default='Clip 1', maxchar=20)
    input_menu.add.button(f'Confirm', end_loop)

    while loop:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        input_menu.update(events)
        input_menu.draw(surface)
        pygame.display.update()

    print(clip_name)
    play(GenerateMode())

def play(game):
    #Game loop
    #game_over=False
    while True:
        game_over,score=game.play_step()
        if(game_over == True):
            break
    print('Final Score',score)

menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Car Game',
    width=400
)

user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
menu.add.button('Game Mode', game_mode)
menu.add.button('Playback Mode', inspect_data)
menu.add.button('Generate Mode', generate_data)
# menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
# menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
