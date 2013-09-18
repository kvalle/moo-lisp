# -*- coding: utf-8 -*-

from errors import LispNamingError
from types import Builtin
import operator as op

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

def get_default_env():
    return Environment({
        '+': Builtin(op.add),
        '-': Builtin(op.sub),
        '*': Builtin(op.mul),
        '/': Builtin(op.div),
        'mod': Builtin(lambda x, y: x % y),

        '=': Builtin(op.eq), 
        '>': Builtin(op.gt), 
        '<': Builtin(op.lt), 
        '>=': Builtin(op.ge), 
        '<=': Builtin(op.le)
    })
