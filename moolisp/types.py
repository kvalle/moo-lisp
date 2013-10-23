# -*- coding: utf-8 -*-

from inspect import getargspec
from errors import LispTypeError

## functions creating and working with types

def tag(tag, value):
    """A typed value is represented by a touple of type and value"""
    return ("type", tag, value)

def is_type(t):
    """Check whether value is typed"""
    return isinstance(t, tuple) \
        and len(t) == 3 \
        and t[0] == "type"

def type_of(x):
    """Get type from a typed value"""
    if not is_type(x):
        raise LispTypeError("Type of non-type: %s" % x)
    return x[1]

def value_of(x):
    """Get value of a typed value"""
    if not is_type(x):
        raise LispTypeError("Value of non-type: %s" % x)
    return x[2]

## 'special' types

def is_symbol(x):
    return isinstance(x, str)

def is_list(x):
    return isinstance(x, list)

def is_atom(x):
    return is_symbol(x) or is_integer(x) or is_boolean(x)

## booleans

def boolean(x):
    return tag('bool', x)
    
def is_boolean(x):
    return is_type(x) and type_of(x) == 'bool'

## integers

def integer(x):
    return tag('int', x)

def is_integer(x):
    return is_type(x) and type_of(x) == 'int'

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
