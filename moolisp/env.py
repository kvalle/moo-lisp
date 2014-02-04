# -*- coding: utf-8 -*-

from errors import LispNamingError
from types import Builtin, boolean, integer, value_of

class Environment(dict):
    def __init__(self, vars=None, outer=None):
        self.outer = outer
        if vars:
            self.update(vars)

    def __getitem__(self, key):
        return self.defining_env(key).get(key)

    def defining_env(self, variable):
        "Find the innermost environment defining a variable"
        if variable in self:
            return self
        elif self.outer is not None:
            return self.outer.defining_env(variable)
        else:
            raise LispNamingError("Variable '%s' is undefined" % variable)

def get_builtin_env():
    """Returns an environment with the builtin functions defined.

    You probably want to use moolisp.interpreter.default_env instead,
    which is this extended with the Moo Lisp core functions."""
    return Environment({
        '+': Builtin(lambda x, y: integer(value_of(x) + value_of(y))),
        '-': Builtin(lambda x, y: integer(value_of(x) - value_of(y))),
        '*': Builtin(lambda x, y: integer(value_of(x) * value_of(y))),
        '/': Builtin(lambda x, y: integer(value_of(x) / value_of(y))),
        'mod': Builtin(lambda x, y: integer(value_of(x) % value_of(y))),

        '=': Builtin(lambda x, y: boolean(x == y)), 
        '>': Builtin(lambda x, y: boolean(x > y)), 
        '<': Builtin(lambda x, y: boolean(x < y)), 
        '>=': Builtin(lambda x, y: boolean(x >= y)), 
        '<=': Builtin(lambda x, y: boolean(x <= y)),

        'cons': Builtin(lambda h, rest: [h] + rest),
        'car': Builtin(lambda lst: lst[0]),
        'cdr': Builtin(lambda lst: 'nil' if len(lst) == 1 else lst[1:]),
        'list': Builtin(lambda *args: 'nil' if len(args) == 0 else list(args))
    })
