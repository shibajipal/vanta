# pipeline.py
# this handles pipelining, i.e., chaining multiple cmds

import io
import sys
import shlex, subprocess
from config import POSIX, builtin
from shell_builtins import builtInCommands

printable = ["pwd", "echo", "type", "history"]

def interceptor(command, args):
    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    builtInCommands[command](args)
    sys.stdout = old_stdout
    captured = buffer.getvalue()
    return captured

def run_pipeline(prompts, initial_input=None):
    processes = []
    last_stdout = None
    
    for i, cmd in enumerate(prompts):
        prompt_parts = shlex.split(cmd, posix=POSIX)
        if i == 0:
            stdin = subprocess.PIPE if initial_input else None
        else:
            stdin = last_stdout
        
        stdout = subprocess.PIPE if i < len(prompts) - 1 else None
        p = subprocess.Popen(prompt_parts, stdin=stdin, stdout=stdout)
        processes.append(p)
        
        if last_stdout:
            last_stdout.close()
        last_stdout = p.stdout
        
    if initial_input:
        if isinstance(initial_input, str):
            initial_input = initial_input.encode()
        processes[0].stdin.write(initial_input)
        processes[0].stdin.close()
    final_output, _ = processes[-1].communicate()
    return final_output.decode() if final_output else ""

def multi_pipelining(prompt):
    prompts = prompt.split("|")
    labels = ["builtin" if shlex.split(x, posix=POSIX)[0] in builtin else "other" for x in prompts]
    if "builtin" not in labels:
        run_pipeline(prompts)
    else:
        last = 0
        for i, label in enumerate(labels):
            if label == "builtin":
                last = i
        prompt = shlex.split(prompts[last], posix=POSIX)
        cmd, args = prompt[0], prompt[1:]
        if last == len(prompts) - 1:
            
            builtInCommands[cmd](args)
        else:
            if cmd in printable:
                value = interceptor(cmd, args)
                run_pipeline(prompts[last + 1:], value)
            else:
                run_pipeline(prompts[last + 1:])

    
        
    
    
    
def dual_pipelining(prompt):
    
    initial, final = prompt.split("|", 1)
    initial = shlex.split(initial.strip(), posix=POSIX)
    final = shlex.split(final.strip(), posix=POSIX)
    cmd1, cmd2 = initial[0], final[0]
    args1, args2 = initial[1:], final[1:]
    # print(cmd1, cmd2)
    if cmd1 not in builtin and cmd2 not in builtin:
        p1 = subprocess.Popen(initial, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(final, stdin=p1.stdout)
        p1.stdout.close()
        p2.communicate()
    elif cmd1 in builtin and cmd2 not in builtin:
        if cmd1 in ["pwd", "type", "echo"]:
            value = interceptor(cmd1, args1)
            p2 = subprocess.Popen(final, stdin=subprocess.PIPE, text=True)
            p2.communicate(input=value)
        else:
            subprocess.Popen(final)
        
        
    elif cmd1 not in builtin and cmd2 in builtin:
        builtInCommands[cmd2](args2)
        
        
    elif cmd1 in builtin and cmd2 in builtin:
        # print("both builtin")
        builtInCommands[cmd2](args2)
