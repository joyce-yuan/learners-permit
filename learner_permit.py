import pygame
import sys
import pygame_menu
from pygame_menu.examples import create_example_window
from car_game import CarGame as GameMode
from car_game_setting_scene import CarGame as InspectDataMode
from car_game_with_screens import CarGame as CreateDataMode


### Trial 2 from https://pygame-menu.readthedocs.io/en/4.2.8/

from typing import Tuple, Any

surface = create_example_window('Example - Simple', (700, 600))


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
    """

    print("Inspect data")
    play(InspectDataMode())

def generate_data() -> None:
    """
    """

    print("Generate data")
    play(CreateDataMode())

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
menu.add.button('Inspect Data', inspect_data)
menu.add.button('Generate Data', generate_data)
# menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
# menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
