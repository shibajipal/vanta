# input_handler.py
# this was the toughest for me, implementing a parser and basically an autocompletion system by scratch
# i proly need to rewrite the autocompletion code logic but it works for now so i aint touching shi


import sys
import os
from config import getch
import config
from colors import colored_text, THEME, RESET, BOLD


def longest_substring(str1, str2):
    answer = 0
    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            break
        answer += 1
    return answer


def _write_colored(text, color):
    sys.stdout.write(f"{color}{text}{RESET}")
    sys.stdout.flush()


def _color_completion(name, is_dir):
    if is_dir:
        return THEME.blue  # directories in blue
    else:
        return THEME.green  # files in green


def _color_match(match):
    # if it ends with / it's a directory
    if match.endswith("/"):
        return colored_text(match, BOLD + THEME.blue)
    else:
        return colored_text(match, THEME.green)


def _write_completion(completion_text, is_dir):
    color = _color_completion(completion_text, is_dir)
    if is_dir:
        _write_colored(completion_text + "/", color)
    else:
        _write_colored(completion_text + " ", color)


def parser(autocomplete_array, start="$ "):
    sys.stdout.write(start)
    sys.stdout.flush()
    buffer, tab_counter = "", 0
    
    while True:

        ch = getch()
        
        if ch in ("\r", "\n"):
            sys.stdout.write(RESET + "\n")
            return buffer
        
        elif ch == "\x03":
            sys.stdout.write(RESET + "\n")
            raise KeyboardInterrupt
        
        elif ch in ("\x08", "\x7f"):
            if len(buffer) > 0:
                buffer = buffer[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
                tab_counter = 0
        elif ch in ('\x00', '\xe0', '\x1b'):
            c = getch()
            if c == '[':
                c2 = getch()
                if c2 == 'A':
                    config.current_line -= 1
                    config.current_line = max(0, config.current_line)
                elif c2 == 'B':
                    config.current_line += 1
                    config.current_line = min(config.current_line, len(config.prompt_history) - 1)
            elif c == 'H':
                config.current_line -= 1
                config.current_line = max(0, config.current_line)
            elif c == 'P':
                config.current_line += 1
                config.current_line = min(config.current_line, len(config.prompt_history) - 1)
            chars_to_delete = len(buffer)
            sys.stdout.write("\b" * chars_to_delete + " " * chars_to_delete + "\b" * chars_to_delete)
            buffer = config.prompt_history[config.current_line]
            # History recall in yellow
            _write_colored(buffer, THEME.yellow)
        elif ch == "\t":
            tab_counter += 1
            if " " in buffer:
                text = buffer.split()[-1] if not buffer.endswith(" ") else ""
                if not text:
                    local_completion_matches = [x for x in os.listdir(os.getcwd())]
                    if len(local_completion_matches) == 1:
                        completion = local_completion_matches[0]
                        buffer += completion
                        if os.path.isdir(os.getcwd() + "/" + completion):
                            buffer += "/"
                            _write_colored(completion + "/", THEME.blue)
                        else:
                            buffer += " "
                            _write_colored(completion + " ", THEME.green)
                        tab_counter = 0
                    tab_counter = 0
                    continue
                if "/" in text:
                    path = "/".join(text.split("/")[:-1])
                    files_in_path = os.listdir(os.getcwd()+"/"+path)
                    written = text.split("/")[-1]
                    local_completion_matches = [x for x in files_in_path if x.startswith(written)]
                    local_completion_matches = sorted(local_completion_matches, key = len)
                    # print("\n written is ", written)
                    # print(local_completion_matches)
                    if len(local_completion_matches) == 1:
                        completion = local_completion_matches[0][len(written):]
                        buffer += completion
                        full_name = written + completion
                        full_path = os.getcwd() + "/" + path + "/" + full_name
                        # Erase the typed part, rewrite full name in color
                        sys.stdout.write("\b" * len(written) + " " * len(written) + "\b" * len(written))
                        if os.path.isdir(full_path):
                            buffer += "/"
                            _write_colored(full_name + "/", THEME.blue)
                        else:
                            buffer += " "
                            _write_colored(full_name + " ", THEME.green)
                        tab_counter = 0
                completion_matches = [x for x in autocomplete_array if x.startswith(text)]
                completion_matches = sorted(completion_matches, key=len)
                
                if len(completion_matches) == 1:
                    completion = completion_matches[0][len(text):]
                    buffer += completion
                    full_name = text + completion
                    sys.stdout.write("\b" * len(text) + " " * len(text) + "\b" * len(text))
                    if os.path.isdir(os.getcwd() + "/" + full_name):
                        # buffer += "/"
                        _write_colored(full_name, THEME.blue)
                    else:
                        buffer += " "
                        _write_colored(full_name + " ", THEME.green)
                    tab_counter = 0
                    
                elif len(completion_matches) > 1:
                    if tab_counter == 1:
                        executables = 0
                        
                        length = len(completion_matches[0])
                        for i in completion_matches:
                            length = min(length, longest_substring(completion_matches[0], i))
                        # print(completion_matches, length)
                        if length > len(text):
                            completion = completion_matches[0][len(text):length]
                            buffer += completion
                            
                            _write_colored(completion, THEME.dark_yellow)
                            tab_counter = 0
                        else:
                            sys.stdout.write("\x07")
                            sys.stdout.flush()
                            # print("\n completion is ", completion)
                    elif tab_counter == 2:
                        colored_matches = [_color_match(m) for m in sorted(completion_matches)]
                        sys.stdout.write("\n" + "  ".join(colored_matches) + "\n")
                        sys.stdout.write(start + THEME.fg + buffer + RESET)
                        sys.stdout.flush()
                        tab_counter = 0
                elif len(completion_matches) == 0:
                    sys.stdout.write("\x07")
                    sys.stdout.flush()
            else:    
                completion_matches = [x for x in autocomplete_array if x.startswith(buffer)]
                completion_matches = sorted(completion_matches, key=len)
                
                if len(completion_matches) == 1:
                    typed_part = buffer
                    completion = completion_matches[0][len(buffer):]
                    buffer += completion
                    full_name = buffer
                    sys.stdout.write("\b" * len(typed_part) + " " * len(typed_part) + "\b" * len(typed_part))
                    if os.path.isdir(os.getcwd() + "/" + full_name):
                        _write_colored(full_name, THEME.blue)
                    else:
                        buffer += " "
                        _write_colored(full_name + " ", THEME.green)
                    
                    tab_counter = 0
                elif len(completion_matches) > 1:
                    # print(completion_matches)
                    if tab_counter == 1:
                        length = len(completion_matches[0])
                        for i in completion_matches:
                            length = min(length, longest_substring(completion_matches[0], i))
                        if length > len(buffer):
                            completion = completion_matches[0][len(buffer):length]
                            buffer += completion
                            
                            _write_colored(completion, THEME.dark_yellow)
                            tab_counter = 0
                        else:
                            sys.stdout.write("\x07")
                            sys.stdout.flush()
                    elif tab_counter == 2:
                        colored_matches = [_color_match(m) for m in sorted(completion_matches)]
                        sys.stdout.write("\n" + "  ".join(colored_matches) + "\n")
                        sys.stdout.write(start + THEME.fg + buffer + RESET)
                        sys.stdout.flush()
                        tab_counter = 0
                elif len(completion_matches) == 0:
                    sys.stdout.write("\x07")
                    sys.stdout.flush()
        elif ch.isprintable():
            buffer += ch
            # User typed text in foreground color
            _write_colored(ch, THEME.fg)
            tab_counter = 0
