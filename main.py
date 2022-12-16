import collections
from typing import Deque
from os import system as sys
from os import name as operating_system
from enum import Enum
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from time import sleep
import utility

INPUT_LAG = 0.2


class GAMESTATE(Enum):
  EXIT = 0
  MAIN_MENU = 1
  GAME_MENU = 2
  PLAY = 3
  GAME_OVER_SCREEN = 4
  SET_PARAMETERS_MENU = 5


class Game:
  STATE = GAMESTATE.MAIN_MENU
  LEVEL = 4
  INVALID_ENTRY = False

  @staticmethod
  def run():
    # Main Loop
    while Game.STATE != GAMESTATE.EXIT:
      if Game.STATE == GAMESTATE.MAIN_MENU:
        Game.clear_screen()
        response = Game.main_menu()
        if response == -1:
          continue
        if response == 1:
          Game.STATE = GAMESTATE.GAME_MENU
        if response == 2:
          Game.STATE = GAMESTATE.EXIT
        continue

      if Game.STATE == GAMESTATE.GAME_MENU:
        Game.game_setup_menu()

      if Game.STATE == GAMESTATE.PLAY:
        # UNUSED ATM
        continue

      if Game.STATE == GAMESTATE.GAME_OVER_SCREEN:
        Game.clear_screen()
        Game.STATE = Game.game_over_screen()
        continue

    print("Goodbye!")

  @staticmethod
  def play_game(number_of_towers, number_of_disks):
    """
    Play Towers of Hanoi
    :param number_of_towers: int representing the number of towers
    :param number_of_disks:  int representing the number of disks
    """
    # Sanity Check
    if number_of_towers < 3 or number_of_disks < 4:
      print("Invalid Game.")
      return

    # Build towers / list of stacks
    towers: [Deque[int]] = []
    for _ in range(0, number_of_towers):
      towers.append(collections.deque())
    for i in range(number_of_disks, 0, -1):
      towers[0].append(i)

    solved = False
    tower_selected = 0
    holding_disk = 0  # 0 is not hold a disk
    while not solved:
      print("Press Escape to quit")

      # Print the state
      print()
      for i, tower in enumerate(towers):
        if i == tower_selected:
          print("X Tower# ", end="")
        else:
          print("  Tower# ", end="")
        print(str(i + 1) + ":", end="")
        for num in tower:
          print(str(num) + "-", end="")
        # Print numbers
        print()

      print()
      if holding_disk >= 1:
        print("You are holding disk: " + str(holding_disk))
      else:
        print("You are not holding a disk.")
      print("Use arrows to move selected tower. (X)")
      print("Use the space to grab the top disk and place it.")

      # Take Input
      with keyboard.Events() as events:
        # Block for as much as possible
        event = events.get(1e6)
        sleep(INPUT_LAG)
        if event.key == keyboard.Key.esc:  # END GAME
          return
        elif event.key == keyboard.Key.up:
          if tower_selected != 0:
            tower_selected -= 1
        elif event.key == keyboard.Key.down:
          if tower_selected != number_of_towers - 1:
            tower_selected += 1
        elif event.key == keyboard.Key.space:
          if len(towers[tower_selected]) != 0 and holding_disk == 0:
            # print("grabbing")
            holding_disk = towers[tower_selected].pop()
          elif holding_disk >= 1:
            # if len(towers[tower_selected]) == 0 or [tower_selected][0] > holding_disk:
            #   towers[tower_selected].append(holding_disk)
            #   holding_disk = 0
            towers[tower_selected].append(holding_disk)
            holding_disk = 0

      # Check if done
      if len(towers[number_of_towers - 1]) == number_of_disks:
        solved = True

    # finish game
    print("CONGRATULATIONS!!! You solved the puzzle!")
    input("Press enter to go to the menu.11 ")
    pass

  @staticmethod
  def main_menu() -> int:
    """
    The Main Menu.
    :returns:
    (1) for Game Setup Menu. <br>
    (2) for Quitting. <br>
    (-1) Error.
    """
    print("Main Menu: ")
    print("  1) Game Setup")
    print("  2) Quit")
    print("Enter Selection #")
    valid_keys = ['1', '2']
    while True:
      with keyboard.Events() as events:
        # Block for as much as possible
        event = events.get(1e6)
        sleep(INPUT_LAG)
        try:
          if event.key.char in valid_keys:
            return int(event.key.char)
        except AttributeError:
          continue

  @staticmethod
  def _set_state(game_state: GAMESTATE):
    Game.STATE = game_state

  @staticmethod
  def game_setup_menu():
    """
    The Game Menu.
    (1) Play an easy game. <br>
    (2) set number of levels. <br>
    (3) Main Menu <br>
    (-1) Error.
    """
    intro = "Game Menu: \n"
    key_options = [KeyCode.from_char('1'),
                   KeyCode.from_char('2'),
                   Key.esc]
    text_options = ["  1) Play Standard Easy Game",
                    "  2) Set number of levels",
                    "Esc) Main Menu"]
    end = ""
    option_function = [lambda _: Game.play_game(number_of_towers=3, number_of_disks=4),
                       lambda _: Game._set_state(GAMESTATE.SET_PARAMETERS_MENU),
                       lambda _: Game._set_state(GAMESTATE.MAIN_MENU)]
    while True:
      response = utility.keystroke_menu(list(zip(key_options, text_options)),
                                        intro_text=intro,
                                        end_text=end)
      print(type(response))
      # if response in key_options:
      #   option_function[key_options.index(response)]()

  @staticmethod
  def game_over_screen():
    print("Game Over")
    input("Hit any key to continue.")
    return GAMESTATE.MAIN_MENU

  @staticmethod
  def clear_screen():
    if operating_system == 'nt':
      sys('cls')
    else:
      sys('clear')


def main():
  Game.run()


if __name__ == '__main__':
  """
  This is the first thing to run in our code.
  Consider it the "door way" to the application
  """
  main()
