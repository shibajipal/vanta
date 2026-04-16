# Vanta Shell

A lightweight, cross-platform shell implementation written in Python. Vanta provides an interactive command-line interface with Unix-like shell features including command pipelining, output redirection, built-in commands, and command history.

## Features

- **Interactive Command-Line Interface** - Dynamic autocompletion system that suggests executables from PATH and local files
- **Built-in Commands** - Implementation of essential shell builtins:
  - `pwd` - Print working directory
  - `cd` - Change directory (including `cd ~`)
  - `echo` - Print arguments
  - `exit` - Gracefully exit the shell
  - `type` - Display command type (builtin or external path)
  - `history` - View and manage command history
- **Command Pipelining** - Chain multiple commands using pipes (`|`)
- **Output Redirection** - Redirect stdout and stderr:
  - `>` or `1>` - Redirect stdout (overwrite)
  - `>>` or `1>>` - Redirect stdout (append)
  - `2>` - Redirect stderr (overwrite)
  - `2>>` - Redirect stderr (append)
- **Command History** - Persistent history management with navigation (↑/↓ arrow keys)
- **Cross-Platform Support** - Works on Windows, macOS, and Linux
- **History Persistence** - Save and load command history from file

## Project Structure

```
vanta/
├── client.py           # Main entry point - orchestrates all components
├── config.py           # Configuration, environment variables, history management
├── input_handler.py    # Command parser with autocompletion system
├── pipeline.py         # Handles command pipelining logic
├── redirection.py      # Manages stdout/stderr redirection
├── shell_builtins.py   # Implementation of built-in shell commands
└── README.md          # This file
```

## Installation

### Requirements
- Python 3.6 or higher

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vanta.git
cd vanta
```

2. Run the shell:
```bash
python client.py
```

## Usage

### Basic Commands

```bash
$ echo Hello World
Hello World

$ pwd
/current/directory

$ cd /path/to/directory

$ type echo
echo is a shell builtin

$ history
    1  echo Hello World
    2  pwd
    3  cd /path/to/directory
```

### Pipelining

Execute multiple commands in sequence, passing output from one command to another:

```bash
$ echo "line1\nline2\nline3" | grep line1

$ cat file.txt | wc -l | echo
```

### Output Redirection

Redirect command output to files:

```bash
$ echo "Hello" > output.txt          # Overwrite file
$ echo "World" >> output.txt         # Append to file
$ command_with_error 2> errors.txt   # Redirect stderr
```

### Command History

Navigate through your command history with arrow keys:
- **↑** - Previous command
- **↓** - Next command

View history:
```bash
$ history              # Show all commands
$ history 10           # Show last 10 commands
$ history -w file.txt  # Write history to file
$ history -r file.txt  # Read history from file
$ history -a file.txt  # Append history to file
```

## Configuration

Environment variables used by Vanta:

- `PATH` - Directory paths to search for executables
- `HOME` - User's home directory (for `cd ~`)
- `HISTFILE` - File path for persistent command history

These are automatically detected from your system configuration.

## Architecture

### Command Processing Pipeline

1. **Input Parsing** (`input_handler.py`)
   - Captures user input character-by-character
   - Provides real-time autocompletion suggestions
   - Handles arrow key navigation through history

2. **Command Parsing** (`client.py`)
   - Tokenizes input using shell-like syntax
   - Detects redirection operators
   - Identifies built-in vs. external commands

3. **Execution Routing**
   - Built-in commands → `shell_builtins.py`
   - External commands → System `subprocess`
   - Piped commands → `pipeline.py`
   - Redirected output → `redirection.py`

### Key Components

#### shell_builtins.py
Implements all built-in commands with lambda-based dispatch dictionary for efficient command lookup.

#### pipeline.py
Supports both:
- **Dual pipelining** - Single pipe operations (`cmd1 | cmd2`)
- **Multi-pipelining** - Multiple pipes with smart builtin/external command handling

#### redirection.py
Handles:
- File creation and opening with appropriate modes (write/append)
- stdout/stderr capture and redirection
- Proper error handling for file operations

#### config.py
- Cross-platform getch() implementation (Windows/Unix)
- Environment variable management
- History file persistence
- POSIX flag for platform-specific shell behavior

## Platform Support

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Basic Commands | ✓ | ✓ | ✓ |
| Pipelining | ✓ | ✓ | ✓ |
| Redirection | ✓ | ✓ | ✓ |
| History | ✓ | ✓ | ✓ |
| Arrow Keys | ✓ | ✓ | ✓ |

## Autocompletion

The shell provides intelligent autocompletion by:
1. Scanning executables in PATH directories
2. Listing files in the current directory
3. Suggesting matches as you type
4. Auto-completing with `/` suffix for directories

Press `TAB` to activate autocompletion.


