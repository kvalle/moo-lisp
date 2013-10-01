# -*- coding: utf-8 -*-

__all__ = ['repl', 'parse_file', 'interpret', 'parse', 'evaluate']

import sys
from evaluator import evaluate
from parser import parse, unparse
from repl import repl
from errors import LispError
from env import get_default_env

def parse_file(filename):
    """Interpret a .moo source file"""
    try:
        with open(filename, 'r') as sourcefile:
            source = "(begin %s)" % "".join(sourcefile.readlines())
            print unparse(interpret(source))
    except LispError, e:
        print e
        sys.exit(1)

def interpret(source, env=None):
    """Interpret a moo-lisp program statement."""
    if env is None:
        env = get_default_env()
    return evaluate(parse(source), env)
