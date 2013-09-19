# -*- coding: utf-8 -*-

from errors import LispError
from colors import colored, faded
from env import get_default_env
from interpreter import interpret, unparse, preprocess

# importing this gives readline goodness when running on systems
# where it is supported (i.e. UNIX-y systems)
import readline   # noqa

def repl():
    """Start the interactive Read-Eval-Print-Loop
    """
    print
    print "                       " + faded("    ^__^             ")
    print "          welcome to   " + faded("    (oo)\_______     ")
    print "         the MOO-lisp  " + faded("    (__)\       )\/\ ")
    print "             REPL      " + faded("        ||----w |    ")
    print "                       " + faded("        ||     ||    ")
    print

    env = get_default_env()
    try:
        while True:
            try:
                source = read_expression()
                if source.strip() == "(help)":
                    with open('moolisp/usage.txt', 'r') as f:
                        print "".join(f.readlines())
                else:
                    result = interpret(source, env)
                    if result is not None: 
                        print unparse(result)
            except LispError, e:
                print colored("! ", "red") + str(e)
    except (EOFError, KeyboardInterrupt):
        print faded("\nBye! o/")

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
