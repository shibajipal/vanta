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
from colors import prompt_text, error_text, BOLD, RESET, colored_text, THEME


# Commands whose output should be colorized as file listings
LS_COMMANDS = {"ls", "dir", "ls.exe", "dir.exe"}


def colorize_ls_output(output, cwd):
    result = []
    for line in output.splitlines():
        words = line.split()
        colored_words = []
        for word in words:
            
            clean = word.rstrip("/\\*@|")
            check_path = os.path.join(cwd, clean)
            try:
                if os.path.isdir(check_path):
                    colored_words.append(f"{BOLD}{THEME.blue}{word}{RESET}")
                elif os.path.isfile(check_path) and os.access(check_path, os.X_OK):
                    colored_words.append(f"{THEME.green}{word}{RESET}")
                elif os.path.islink(check_path):
                    colored_words.append(f"{THEME.cyan}{word}{RESET}")
                else:
                    colored_words.append(f"{THEME.fg}{word}{RESET}")
            except (OSError, ValueError):
                colored_words.append(f"{THEME.fg}{word}{RESET}")
        result.append("  ".join(colored_words))
    return "\n".join(result) + "\n"


def colorize_output(command, output, cwd):
    
    base_cmd = os.path.basename(command).lower()
    if base_cmd in LS_COMMANDS:
        return colorize_ls_output(output, cwd)
    else:
        return f"{THEME.fg}{output}{RESET}"


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
        prompt_symbol = colored_text("$ ", BOLD + THEME.green)
        prompt = parser(autocomplete_array, prompt_symbol)
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
            result = subprocess.run(prompt_parts, text=True, capture_output=True, executable=path)
            if result.stdout:
                sys.stdout.write(colorize_output(command, result.stdout, curr_dir))
            if result.stderr:
                sys.stderr.write(THEME.red + result.stderr + RESET)
        elif command in builtin:
            builtInCommands[command](args)
        else:
            print(error_text(f"{command}: command not found"))


if __name__ == "__main__":
    main()
