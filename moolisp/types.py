# -*- coding: utf-8 -*-

from inspect import getargspec

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
