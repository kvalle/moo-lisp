# -*- coding: utf-8 -*-

from errors import LispSyntaxError, LispTypeError
from env import Environment
from types import Closure, Lambda, Builtin 
from parser import unparse

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if isinstance(ast, str):
        return env[ast]
    elif not isinstance(ast, list):
        return ast
    elif ast[0] == 'if': 
        _assert_exp_length(ast, 4)
        (_, pred, then_exp, else_exp) = ast
        return evaluate((then_exp if evaluate(pred, env) else else_exp), env)
    elif ast[0] == 'eval':
        _assert_exp_length(ast, 2)
        (_, exp) = ast
        return evaluate(evaluate(exp, env), env)
    elif ast[0] == 'define': 
        _assert_exp_length(ast, 3)
        (_, variable, expression) = ast
        env[variable] = evaluate(expression, env)
    elif ast[0] == 'lambda' or ast[0] == 'λ':
        _assert_exp_length(ast, 3)
        (_, params, body) = ast
        return Lambda(params, body, env)
    elif ast[0] == 'begin':
        if len(ast[1:]) == 0:
            raise LispSyntaxError("begin cannot be empty: %s" % unparse(ast))
        results = [evaluate(exp, env) for exp in ast[1:]]
        return results[-1]
    elif ast[0] == 'quote':
        _assert_exp_length(ast, 2)
        (_, exp) = ast
        return exp
    elif ast[0] == 'set!':
        _assert_exp_length(ast, 3)
        (_, var, exp) = ast
        env.defining_env(var)[var] = evaluate(exp, env)
    else:
        cls = evaluate(ast[0], env)
        if not isinstance(cls, Closure):
            raise LispTypeError("Call to non-function: " + unparse(ast))

        args = [evaluate(exp, env) for exp in ast[1:]]
        if isinstance(cls, Lambda):
            if len(args) != len(cls.params):
                msg = "Wrong number of arguments, expected %d got %d: %s" \
                    % (len(cls.params), len(args), unparse(ast))
                raise LispTypeError(msg)
            return evaluate(cls.body, Environment(zip(cls.params, args), env))
        elif isinstance(cls, Builtin):
            return cls.fn(*args)
        else:
            raise Exception("Unknown implementation of Closure: %s" % cls)

def _assert_exp_length(ast, length):
    if len(ast) > length:
        msg = "Malformed %s, too many arguments: %s" % (ast[0], unparse(ast))
        raise LispSyntaxError(msg)
    elif len(ast) < length:
        msg = "Malformed %s, too few arguments: %s" % (ast[0], unparse(ast))
        raise LispSyntaxError(msg)
