# colors.py
# Custom color theme for Vanta shell

# ANSI escape codes for 24-bit true color (RGB)
def rgb(r, g, b):
    """Generate ANSI escape code for RGB color"""
    return f"\033[38;2;{r};{g};{b}m"

def bg_rgb(r, g, b):
    """Generate ANSI escape code for RGB background color"""
    return f"\033[48;2;{r};{g};{b}m"

# Reset code
RESET = "\033[0m"
BOLD = "\033[1m"


class DarkTheme:
    # Background
    bg = bg_rgb(40, 40, 40)  # #282828
    
    # Foreground
    fg = rgb(235, 219, 178)  # #ebdbb2
    
    # Colors
    dark_red = rgb(204, 36, 29)  # #cc241d
    red = rgb(251, 73, 52)  # #fb4934
    
    dark_green = rgb(152, 151, 26)  # #98971a
    green = rgb(184, 187, 38)  # #b8bb26
    
    dark_yellow = rgb(215, 153, 33)  # #d79921
    yellow = rgb(250, 189, 47)  # #fabd2f
    
    dark_blue = rgb(69, 133, 136)  # #458588
    blue = rgb(131, 165, 152)  # #83a598
    
    dark_purple = rgb(177, 98, 134)  # #b16286
    purple = rgb(211, 134, 155)  # #d3869b
    
    dark_cyan = rgb(104, 157, 106)  # #689d6a
    cyan = rgb(142, 192, 124)  # #8ec07c
    
    dark_gray = rgb(168, 153, 132)  # #a89984
    gray = rgb(146, 131, 116)  # #928374

class LightTheme:
    # Background
    bg = bg_rgb(249, 245, 215)  # #f9f5d7
    
    # Foreground
    fg = rgb(60, 56, 54)  # #3c3836
    
    # Colors (lighter variants for light background)
    dark_red = rgb(157, 0, 6)  # #9d0006
    red = rgb(204, 36, 29)  # #cc241d
    
    dark_green = rgb(79, 74, 0)  # #4f4a00
    green = rgb(98, 97, 1)  # #626105
    
    dark_yellow = rgb(181, 118, 20)  # #b57614
    yellow = rgb(215, 153, 33)  # #d79921
    
    dark_blue = rgb(7, 102, 120)  # #076678
    blue = rgb(69, 133, 136)  # #458588
    
    dark_purple = rgb(143, 63, 113)  # #8f3f71
    purple = rgb(177, 98, 134)  # #b16286
    
    dark_cyan = rgb(66, 124, 113)  # #427c71
    cyan = rgb(104, 157, 106)  # #689d6a
    
    dark_gray = rgb(146, 131, 116)  # #928374
    gray = rgb(168, 153, 132)  # #a89984

# Default to dark theme
THEME = DarkTheme

def set_theme(theme_name="dark"):

    global THEME
    if theme_name.lower() == "light":
        THEME = LightTheme
    else:
        THEME = DarkTheme

def colored_text(text, color):
    
    return f"{color}{text}{RESET}"

def prompt_text(text="$ "):
    
    return colored_text(text, BOLD + THEME.green)

def success_text(text):
    return colored_text(text, THEME.green)

def error_text(text):
    return colored_text(text, THEME.red)

def info_text(text):
    return colored_text(text, THEME.blue)

def warning_text(text):
    return colored_text(text, THEME.yellow)

def dir_text(text):
    return colored_text(text, THEME.blue)

def command_text(text):
    return colored_text(text, THEME.purple)

def path_text(text):
    return colored_text(text, THEME.cyan)

