# -*- coding: utf-8 -*-

import cmd

from errors import LispError
from colors import colored, grey
from env import default_environment
from interpreter import interpret, to_string

def repl():
    "Start the interactive Read-Eval-Print-Loop"
    REPL().cmdloop()

class REPL(cmd.Cmd, object):

    prompt = colored("→  ", "grey")
    env = default_environment

    def emptyline(self):
        pass

    def default(self, line):
        "Handle parsing of LISPy inputs"
        try:
            result = interpret(line, self.env)
            if result is not None: 
                print to_string(result)
        except LispError, e:
            print colored("! ", "red") + str(e)

    def do_EOF(self, s):
        "Exit REPL on ^D"
        return True

    def do_help(self, s):
        with open("README.txt", "r") as f:
            for line in f:
                print line,

    def preloop(self):
        print
        print "                       " + grey("    ^__^             ")
        print "          welcome to   " + grey("    (oo)\_______     ")
        print "         the MOO-lisp  " + grey("    (__)\       )\/\ ")
        print "             REPL      " + grey("        ||----w |    ")
        print "                       " + grey("        ||     ||    ")
        print
        super(REPL, self).preloop()

    def postloop(self):
        print grey('\nBye! o/')
        super(REPL, self).postloop()
