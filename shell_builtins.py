# shell_builtins.py
# this is where i implemented sort of builtin cmds like pwd, cd, type, echo etc.

import os
import sys
import shutil
from config import HISTFILE, HOME, old_lines, builtin
import config
from colors import error_text, info_text, dir_text, success_text, command_text, path_text, colored_text, THEME, BOLD, RESET

def handle_exit():
    if HISTFILE:
        with open(HISTFILE, "a") as history_file:
            history_file.writelines("\n".join(config.prompt_history[old_lines:]))
            history_file.writelines("\n")
    sys.exit(0)
        
def typeBuiltIn(cmd):
    if cmd in builtInCommands:
        print(command_text(cmd) + info_text(" is a shell builtin"))
    elif path := shutil.which(cmd):
        print(command_text(cmd) + info_text(" is ") + path_text(path))
    else:
        print(error_text(f"{cmd}: not found"))
        

def cdBuiltIn(cmd):
    if cmd == "~":
        os.chdir(HOME)
    elif os.path.isdir(cmd):
        os.chdir(cmd)
    else:
        print(error_text(f"{cmd}: No such file or directory"))
        

def history_builtin(args):
    start = 0
    
    if args:
        
        if len(args) == 1:
            start = len(config.prompt_history) - int(args[0]) if len(config.prompt_history) - int(args[0]) >= 0 else 0
        else:
            mode, file = args
            if mode == "-r":
                f = open(file, "r")
                content = f.read()
                config.prompt_history.extend(content.split("\n")[:-1])
                return
            elif mode == "-w":
                
                f = open(file, "w")
                f.writelines("\n".join(config.prompt_history))
                f.writelines("\n")
                return
            elif mode == "-a":
                f = open(file, "a")
                f.writelines("\n".join(config.prompt_history[config.last_appended:]))
                f.writelines("\n")
                config.last_appended = len(config.prompt_history)
                return
                
                
    else:
        start = 0
    
    for i, prompt in enumerate(config.prompt_history[start:]):
        index_text = colored_text(str(i + start + 1).rjust(4), THEME.dark_gray)
        print(index_text + colored_text("  ", THEME.dark_gray) + colored_text(prompt, THEME.fg))
    
    return

builtInCommands = {
    "exit" : lambda x : handle_exit(),
    "pwd" : lambda x : print(dir_text(os.getcwd())),
    "cd" : lambda x: cdBuiltIn(" ".join(x)),
    "type" : lambda x: typeBuiltIn(" ".join(x)),
    "echo" : lambda x: print(colored_text(" ".join(x), THEME.fg)),
    "history" : lambda x : history_builtin(x)
}
