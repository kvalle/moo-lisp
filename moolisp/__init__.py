# -*- coding: utf-8 -*-

__all__ = ['repl', 'parse_file', 'interpret', 'parse', 'evaluate']

import sys
from evaluator import evaluate
from parser import parse, unparse
from repl import repl
from errors import LispError
from env import get_builtin_env

def parse_file(filename):
    """Interpret a .moo source file"""
    try:
        with open(filename, 'r') as sourcefile:
            source = "(begin %s)" % "".join(sourcefile.readlines())
            print interpret(source, get_builtin_env())
    except LispError, e:
        print e
        sys.exit(1)

def interpret(source, env):
    """Interpret a moo-lisp program statement, returning the result, both as strings."""
    return unparse(evaluate(parse(source), env))
