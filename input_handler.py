# input_handler.py
# this was the toughest for me, implementing a parser and basically an autocompletion system by scratch
# i proly need to rewrite the autocompletion code logic but it works for now so i aint touching shi


import sys
import os
from config import getch
import config


def longest_substring(str1, str2):
    answer = 0
    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            break
        answer += 1
    return answer

def parser(autocomplete_array, start="$ "):
    sys.stdout.write(start)
    sys.stdout.flush()
    buffer, tab_counter = "", 0
    
    while True:

        ch = getch()
        
        if ch in ("\r", "\n"):
            sys.stdout.write("\n")
            return buffer
        
        elif ch == "\x03":
            sys.stdout.write("\n")
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
            sys.stdout.write(buffer)
            sys.stdout.flush()
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
                            sys.stdout.write(completion + "/")
                        else:
                            buffer += " "
                            sys.stdout.write(completion + " ")
                        sys.stdout.flush()
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
                        if os.path.isdir(os.getcwd() + "/" + path + "/" + written + completion):
                            
                            
                            buffer += "/"
                            sys.stdout.write(completion + "/")
                        else:
                            buffer += " "
                            sys.stdout.write(completion + " ")
                        sys.stdout.flush()
                        tab_counter = 0
                completion_matches = [x for x in autocomplete_array if x.startswith(text)]
                completion_matches = sorted(completion_matches, key=len)
                
                if len(completion_matches) == 1:
                    completion = completion_matches[0][len(text):]
                    buffer += completion
                    if os.path.isdir(os.getcwd() + "/" + text + completion):
                        # buffer += "/"
                        sys.stdout.write(completion)
                    else:
                        buffer += " "
                        sys.stdout.write(completion + " ")
                    sys.stdout.flush()
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
                            
                            sys.stdout.write(completion)
                            sys.stdout.flush()
                            tab_counter = 0
                        else:
                            sys.stdout.write("\x07")
                            sys.stdout.flush()
                            # print("\n completion is ", completion)
                    elif tab_counter == 2:
                        sys.stdout.write("\n" + "  ".join(sorted(completion_matches)) + "\n")
                        sys.stdout.write(start + buffer)
                        sys.stdout.flush()
                        tab_counter = 0
                elif len(completion_matches) == 0:
                    sys.stdout.write("\x07")
                    sys.stdout.flush()
            else:    
                completion_matches = [x for x in autocomplete_array if x.startswith(buffer)]
                completion_matches = sorted(completion_matches, key=len)
                
                if len(completion_matches) == 1:
                    completion = completion_matches[0][len(buffer):]
                    buffer += completion
                    if os.path.isdir(os.getcwd() + "/" + buffer):
                        sys.stdout.write(completion)
                    else:
                        buffer += " "
                        sys.stdout.write(completion + " ")
                    sys.stdout.flush()
                    
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
                            
                            sys.stdout.write(completion)
                            sys.stdout.flush()
                            tab_counter = 0
                        else:
                            sys.stdout.write("\x07")
                            sys.stdout.flush()
                    elif tab_counter == 2:
                        sys.stdout.write("\n" + "  ".join(sorted(completion_matches)) + "\n")
                        sys.stdout.write(start + buffer)
                        sys.stdout.flush()
                        tab_counter = 0
                elif len(completion_matches) == 0:
                    sys.stdout.write("\x07")
                    sys.stdout.flush()
        elif ch.isprintable():
            buffer += ch
            sys.stdout.write(ch)
            sys.stdout.flush()
            tab_counter = 0
