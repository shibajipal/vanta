# config.py
# this is the basic configuration file to find the env variables and access the history file

import os
import sys

try:
    import msvcrt
    def getch():
        return msvcrt.getwch()
except ImportError:
    import tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

POSIX = os.name != 'nt'

HOME = os.getenv("HOME")
PATH = os.getenv("PATH")
HISTFILE = os.getenv("HISTFILE")

builtin = ["echo", "exit", "type", "pwd", "cd"]

autocomplete_set = set(builtin)

prompt_history = []

if HISTFILE:
    try:
        with open(HISTFILE, "r") as history_file:
            content = history_file.read()
            
            if content:
                prompt_history = content.split("\n")[:-1]
    except FileNotFoundError:
        pass
old_lines = len(prompt_history)
current_line = 0
last_appended = 0
autocomplete_array = list(autocomplete_set)
