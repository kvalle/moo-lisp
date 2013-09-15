# -*- coding: utf-8 -*-

import operator as op
from errors import LispNamingError

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

default_environment = Environment({
    "*": op.mul, "-": op.sub, "+": op.add, "/": op.div,
    '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq, 'not': op.not_
})