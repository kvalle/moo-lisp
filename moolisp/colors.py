# -*- coding: utf-8 -*-

import os

ATTRIBUTES = {
    'bold': 1, 
    'dark': 2
}

COLORS = {
    'grey': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}

def colored(text, color, attr=None):
    if os.getenv('ANSI_COLORS_DISABLED'):
        return text

    format = '\033[%dm'

    color = format % COLORS[color]
    attr = format % ATTRIBUTES[attr] if attr is not None else ""
    reset = '\033[0m'

    return color + attr + text + reset

def grey(text):
    return colored(text, "grey", attr='bold')
