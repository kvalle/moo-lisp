# -*- coding: utf-8 -*-

from os.path import dirname, join

from evaluator import evaluate
from parser import parse, unparse, parse_multiple
from env import get_builtin_env

def interpret(source, env=None):
    """
    Interpret a moo lisp program statement

    Accepts a moo program statement as a string, interprets it, and then
    returns the resulting moo lisp expression as string.
    """
    if env is None:
        env = default_env()

    return unparse(evaluate(parse(source), env))

def interpret_file(filename, env=None):
    """
    Interpret a moo lisp file

    Accepts a file name of a moo lisp files containing a series
    of moo lisp statements. Returns the value of the last expression
    of the file.
    """
    if env is None:
        env = default_env()

    with open(filename, 'r') as sourcefile:
        source = "".join(sourcefile.readlines())

    asts = parse_multiple(source)
    results = [evaluate(ast, env) for ast in asts]
    return unparse(results[-1])

def default_env():
    """Returns the base moo lisp environment"""
    env = get_builtin_env()
    interpret_file(join(dirname(__file__), '..', 'core.moo'), env)
    return env
