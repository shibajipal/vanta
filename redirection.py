# redirection.py
# this handles the > and >> redirection

import sys
import shutil
import subprocess
from config import builtin
from shell_builtins import builtInCommands


def handle_stdout_redirect(prompt_parts, command, args, redir_target, token):
    """Handle stdout redirection (>, 1>, >>, 1>>)."""
    try:
        if token in (">", "1>"):
            f = open(redir_target, 'w')
        else:
            f = open(redir_target, 'a')
    except Exception:
        print(f"{command}: {redir_target}: No such file or directory")
        return

    if path := shutil.which(command):
        try:
            subprocess.run(prompt_parts, text=True, check=True, executable=path, stdout=f)
        except subprocess.CalledProcessError:
            pass
    elif command in builtin:
        saved_stdout = sys.stdout
        sys.stdout = f
        try:
            builtInCommands[command](args)
        finally:
            sys.stdout = saved_stdout
    else:
        print(f"{command}: command not found")

    f.close()


def handle_stderr_redirect(prompt_parts, command, redir_target, token):
    """Handle stderr redirection (2>, 2>>)."""
    try:
        if token == "2>":
            f = open(redir_target, "w")
        else:
            f = open(redir_target, "a")
    except Exception:
        print(f"{command}: {redir_target}: No such file or directory")
        return
    if path := shutil.which(command):
        try:
            subprocess.run(prompt_parts, text=True, check=True, executable=path, stderr=f)
        except subprocess.CalledProcessError:
            pass
    f.close()


def parse_redirection(prompt_parts, tokens):
    """Parse redirection tokens from prompt_parts. Returns (redir_target, token, modified prompt_parts)."""
    redir_target = None
    matched_token = ""
    for token in tokens:
        if token in prompt_parts:
            idx = prompt_parts.index(token)
            if idx + 1 < len(prompt_parts):
                redir_target = prompt_parts[idx + 1]
                del prompt_parts[idx:idx+2]
            else:
                redir_target = None
            matched_token = token
            break
    return redir_target, matched_token, prompt_parts
