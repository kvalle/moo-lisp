# -*- coding: utf-8 -*-

import sys
from errors import LispError
from colors import colored, faded
from parser import remove_comments
from interpreter import interpret, default_env

# importing this gives readline goodness when running on systems
# where it is supported (i.e. UNIX-y systems)
import readline   # noqa

def repl():
    """Start the interactive Read-Eval-Print-Loop"""
    print
    print "                       " + faded("    ^__^             ")
    print "          welcome to   " + faded("    (oo)\_______     ")
    print "         the MOO-lisp  " + faded("    (__)\       )\/\ ")
    print "             REPL      " + faded("        ||----w |    ")
    print "                       " + faded("        ||     ||    ")
    print faded("  use ^D to exit")
    print

    env = default_env()
    while True:
        try:
            source = read_expression()
            print interpret(source, env)
        except LispError, e:
            print colored("!", "red"),
            print faded(str(e.__class__.__name__) + ":"),
            print str(e)
        except KeyboardInterrupt:
            msg = "Interupted. " + faded("(Use ^D to exit)")
            print "\n" + colored("! ", "red") + msg
        except EOFError:
            print faded("\nBye! o/")
            sys.exit(0)
        except Exception, e:
            print colored("! ", "red") + faded("The Python is showing through…")
            print faded("  " + str(e.__class__.__name__) + ":"),
            print str(e)

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
    line = remove_comments(line + "\n")
    return (line, line.count("(") - line.count(")"))
