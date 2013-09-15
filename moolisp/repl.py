# -*- coding: utf-8 -*-

import copy

from errors import LispError
from colors import colored, grey
from env import default_environment
from interpreter import interpret, to_string, preprocess

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
    while True:
        line, parens = read_line("→  " if not exp.strip() else "…  ")
        open_parens += parens
        exp += line
        if exp.strip() and open_parens <= 0:
            break

    return exp

def read_line(prompt):
    "Return touple of user input line and number of unclosed parens"

    line = raw_input(colored(prompt, "grey", "bold"))
    line = preprocess(line + "\n")
    return (line, line.count("(") - line.count(")"))
