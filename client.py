# client.py
# this is the main program to run, attaches everything together!


import os
import sys
import shlex
import shutil
import subprocess

import config
from config import POSIX, builtin
from shell_builtins import builtInCommands
from input_handler import parser
from pipeline import dual_pipelining, multi_pipelining
from redirection import parse_redirection, handle_stdout_redirect, handle_stderr_redirect


def main():
    builtin = ["echo", "exit", "type", "pwd", "cd", "history"]
    
    while True:
        curr_dir = os.getcwd()
        # Rebuild autocomplete array from scratch each iteration
        autocomplete_set = set(builtin)
        # Add executables from PATH
        current_path = os.getenv("PATH", "")
        if current_path:
            for directory in current_path.split(os.pathsep):
                if os.path.isdir(directory):
                    try:
                        for f in os.listdir(directory):
                            full_path = os.path.join(directory, f)
                            if os.path.isfile(full_path):
                                autocomplete_set.add(f)
                    except (PermissionError, OSError):
                        pass
        # Add files in current directory
        autocomplete_set.update(os.listdir(curr_dir))
        autocomplete_array = list(autocomplete_set)
        for i in range(0, len(autocomplete_array)):
            if os.path.isdir(os.getcwd() + "/" + autocomplete_array[i]):
                autocomplete_array[i] += "/"
        # print(autocomplete_array)
        prompt = parser(autocomplete_array, "$ ")
        config.prompt_history.append(prompt)
        config.current_line = len(config.prompt_history)
        prompt_parts = shlex.split(prompt, posix=POSIX)

        # print(autocomplete_array)
        # detect output redirection (>, 1>) and extract target
        redir_target, token, prompt_parts = parse_redirection(prompt_parts, (">", "1>", ">>", "1>>"))

        if not prompt_parts:
            continue

        command = prompt_parts[0]
        args = prompt_parts[1:]
        
        if redir_target:
            handle_stdout_redirect(prompt_parts, command, args, redir_target, token)
            continue
        
        
        redir_target, token, prompt_parts = parse_redirection(prompt_parts, ("2>", "2>>"))
        if not prompt_parts:
            continue
        
        if redir_target:
            handle_stderr_redirect(prompt_parts, command, redir_target, token)
            continue
        
        if "|" in prompt:
            if prompt.count("|") == 1:
                dual_pipelining(prompt)
            else:
                multi_pipelining(prompt)
        elif path := shutil.which(command):
            result = subprocess.run(prompt_parts, text=True, check=True, executable=path)
        elif command in builtin:
            builtInCommands[command](args)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
