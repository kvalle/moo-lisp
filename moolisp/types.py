# -*- coding: utf-8 -*-

class Closure:
    "Abstract base type for builtins and lambdas"
    pass

class Builtin(Closure):
    def __init__(self, fn):
        self.fn = fn

class Lambda(Closure):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
