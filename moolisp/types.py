# -*- coding: utf-8 -*-

from inspect import getargspec
from errors import LispTypeError

## functions for working with types

def tag(tag, value):
    return ("type", tag, value)

def is_type(t):
    return isinstance(t, tuple) \
        and len(t) == 3 \
        and t[0] == "type"

def type_of(x):
    if not is_type(x):
        raise LispTypeError("Type of non-type: %s" % x)
    return x[1]

def value_of(x):
    if not is_type(x):
        raise LispTypeError("Value of non-type: %s" % x)
    return x[2]

## helper functions for built in types

def boolean(x):
    return tag('bool', x)
    
true = boolean(True)
false = boolean(False)

def is_boolean(x):
    return is_type(x) and type_of(x) == 'bool'

def integer(x):
    return tag('int', x)

def is_integer(x):
    return is_type(x) and type_of(x) == 'int'

def symbol(x):
    return tag('symbol', x)

## function helper classes

class Closure:
    "Abstract base type for builtins and lambdas"
    pass

class Builtin(Closure):
    def __init__(self, fn):
        self.fn = fn

    def __str__(self):
        argspec = getargspec(self.fn)
        nargs = len(argspec.args)
        is_vararg = "+" if argspec.varargs else ""
        return "<builtin/%d%s>" % (nargs, is_vararg)

class Lambda(Closure):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __str__(self):
        return "<lambda/%d>" % len(self.params)
