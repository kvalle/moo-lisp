# -*- coding: utf-8 -*-

__all__ = ['repl', 'parse_file', 'interpret', 'tokenize', 'parse', 'evaluate']

import sys
from interpreter import interpret, tokenize, parse, evaluate
from repl import repl
from env import default_environment
from errors import LispError

def parse_file(filename):
    "Interpret a .moo source file"
    try:
        with open(filename, 'r') as sourcefile:
            source = "(begin %s)" % "".join(sourcefile.readlines())
            print interpret(source, default_environment)
    except LispError, e:
        print e
        sys.exit(1)
