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
    "Start the interactive Read-Eval-Print-Loop"
    
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
                line = raw_input(colored("→  ", "grey"))
                result = interpret(line, env)
                if result is not None: 
                    print to_string(result)
            except LispError, e:
                print colored("! ", "red") + str(e)
    except (EOFError, KeyboardInterrupt):
        print colored("\nBye! o/", "grey")
