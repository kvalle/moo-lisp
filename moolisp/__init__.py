# -*- coding: utf-8 -*-

__all__ = ['repl', 'parse_file', 'interpret', 'parse', 'evaluate']

from evaluator import evaluate
from parser import parse, unparse, parse_multiple
from repl import repl
from env import get_builtin_env

def parse_file(filename, env=None):
    if env is None:
        env = get_builtin_env()

    with open(filename, 'r') as sourcefile:
        source = "".join(sourcefile.readlines())

    asts = parse_multiple(source)
    results = [evaluate(ast, env) for ast in asts]
    return unparse(results[-1])

def interpret(source, env):
    """Interpret a moo-lisp program statement, returning the result, both as strings."""
    return unparse(evaluate(parse(source), env))
