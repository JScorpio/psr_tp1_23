#!/usr/bin/env python3
# --------------------------------------------------
# First Practical Project
# João Carvalho, #mec: 106310
# PSR, 12 October 2023.
# --------------------------------------------------


# Imports
    # Colorama
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
    # Time
from time import time, ctime
    # Pretty Print
from pprint import pprint
    # Argparse for help message and arguments
import argparse
    # Read keys
from readchar import readkey, key
    # Letters and Random
import string
import random
    # Named Tuples
from collections import namedtuple

# Sources
    # https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python


# Naming scheme
# variables name_of_variable
# functions nameOfFunction


# Defining named tuple "Input"
Input = namedtuple('Input', ['requested', 'received', 'duration'])


# Functions
def getInput(message=""):
    """
    Get user input with a prompt message
    :param message: the string printed for the prompt
    :return: tuple with the pressed key and the elapsed time from request to keypress
    """
    print(message)
    key_start_time = time()
    pressed_key = readkey()
    key_stop_time = time()
    key_duration = key_stop_time - key_start_time
    return (pressed_key, key_duration)


def main():
    # Defining the parser
    parser = argparse.ArgumentParser(
        description='Typer test. The program tests the user for typing accuracy on the keyboard.')
    parser.add_argument('-utm','--use_time_mode', action='store_true',
        help='Set game to time mode. Defaults to input mode.')
    parser.add_argument('-mv','--max_value', type=ascii, required=False, default=10,
        help='Max number of seconds for time mode or maximum number of inputs for input mode until the game stops.')
    args = vars(parser.parse_args())


    # Variables
    number_of_types = 0
    number_of_hits = 0
    type_hit_duration = 0
    type_miss_duration = 0
    list_of_inputs = []
    in_time_mode = args['use_time_mode']


    # Request user to press any key to start the game
    if in_time_mode:
        print(f"Playing in time mode for {args['max_value']} seconds")
    else:
        print(f"Playing in inputs mode for {args['max_value']} key presses")
    print(f"Press any key to start the game\nPress space bar to stop the game")
    pressed_key = readkey()
    print(f"The game has started!")
    test_start = time()


    elapsed_time = 0
    # Request user to press space key to stop the game
    while not pressed_key == key.SPACE:
        requested_key = random.choice(string.ascii_lowercase)
        (pressed_key, key_duration) = getInput(f"Press key {requested_key}")
        number_of_types += 1
        # 'Input', ['requested', 'received', 'duration']
        list_of_inputs.append(Input(requested_key, pressed_key, key_duration))

        if requested_key == pressed_key:
            number_of_hits += 1
            type_hit_duration += key_duration
            print(f"You pressed key = {Fore.GREEN}{pressed_key}")
        else: # wrong key press
            type_miss_duration += key_duration
            print(f"You pressed key = {Fore.RED}{pressed_key}")

        if in_time_mode and elapsed_time > args['max_value']:
            break
        elif not in_time_mode and number_of_types >= args['max_value']:
            break

        elapsed_time = time() - test_start


    # Removing space bar from the counters
    if pressed_key == key.SPACE:
        if number_of_types > 0:
            number_of_types -= 1
        if len(list_of_inputs) > 0:
            list_of_inputs.pop()


    # Summing up times
    test_end = time()
    test_duration = test_end - test_start

    try:
        accuracy = number_of_hits / number_of_types
    except ZeroDivisionError:
        accuracy = 0

    # Summing up types
    number_of_misses = number_of_types - number_of_hits

    # Summing up averages
    try:
        type_hit_average_duration = type_hit_duration / number_of_hits
    except ZeroDivisionError:
        type_hit_average_duration = 0

    try:
        type_miss_average_duration = type_miss_duration / number_of_misses
    except ZeroDivisionError:
        type_miss_average_duration = 0

    try:
        type_average_duration = (type_hit_duration + type_miss_duration) / number_of_types
    except ZeroDivisionError:
        type_average_duration = 0


    # Creating dictionary
    output_dict = {
        "accuracy": accuracy,
        "number_of_hits": number_of_hits,
        "number_of_misses": number_of_misses,
        "test_duration": test_duration,
        "test_start": ctime(test_start),
        "test_end": ctime(test_end),
        "type_average_duration": type_average_duration,
        "type_hit_average_duration": type_hit_average_duration,
        "type_miss_average_duration": type_miss_average_duration,
        "list_of_inputs": list_of_inputs
    }


    print(f"You have played for {test_duration:.2f} seconds with accuracy {accuracy}")
    print(f"The game has ended")
    pprint(output_dict)




if __name__ == "__main__":
    main()
