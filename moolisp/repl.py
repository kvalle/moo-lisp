# -*- coding: utf-8 -*-

import copy

from errors import LispError
from colors import colored, grey
from env import default_environment
from interpreter import interpret, to_string

# importing this gives readline goodness when running on systems
# where it is supported (i.e. UNIX-y systems)
import readline   # noqa

def repl():
    """Start the interactive Read-Eval-Print-Loop
    """
    print
    print "                       " + grey("    ^__^             ")
    print "          welcome to   " + grey("    (oo)\_______     ")
    print "         the MOO-lisp  " + grey("    (__)\       )\/\ ")
    print "             REPL      " + grey("        ||----w |    ")
    print "                       " + grey("        ||     ||    ")
    print

    env = copy.deepcopy(default_environment)
    try:
        while True:
            try:
                source = read_expression()
                result = interpret(source, env)
                if result is not None: 
                    print to_string(result)
            except LispError, e:
                print colored("! ", "red") + str(e)
    except (EOFError, KeyboardInterrupt):
        print colored("\nBye! o/", "grey")

def read_expression():
    "Read from stdin until we have at least one s-expression"

    exp = ""
    open_parens = 0
    line, parens = read_line("→  ")
    open_parens += parens
    exp += line
    while open_parens > 0:
        line, parens = read_line("…  ")
        open_parens += parens
        exp += line
    return exp

def read_line(prompt):
    "Return touple of user input line and number of unclosed parens"

    line = raw_input(colored(prompt, "grey", "bold"))
    return (line, line.count("(") - line.count(")"))
