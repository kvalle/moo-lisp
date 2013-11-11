# -*- coding: utf-8 -*-

from errors import LispSyntaxError, LispTypeError
from env import Environment
from types import Closure, Lambda, Builtin, Macro
from types import value_of, boolean, is_boolean, is_integer, is_atom, is_symbol, is_list
from types import is_macro, is_closure, is_lambda, is_builtin
from parser import unparse

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_symbol(ast): return env[ast]
    elif is_atom(ast): return ast
    elif is_list(ast):
        if ast[0] == 'macro': return _macro(ast, env)
        elif ast[0] == 'expand': return _expand(ast, env)
        elif ast[0] == 'expand-1': return _expand_1(ast, env)
        elif ast[0] == 'cond': return _cond(ast, env)
        elif ast[0] == 'let': return _let(ast, env)
        elif ast[0] == 'eval': return _eval(ast, env)
        elif ast[0] == 'set!': return _set(ast, env)
        elif ast[0] in ('quote', 'unquote', 'quasiquote'): return _quote(ast, env)
        elif ast[0] in ('lambda', 'λ'): return _lambda(ast, env)
        elif ast[0] == 'atom': return _atom(ast, env)
        elif ast[0] == 'begin': return _begin(ast, env)
        elif ast[0] == 'define': return _define(ast, env)
        elif ast[0] == 'if': return _if(ast, env)
        else: return _apply(ast, env)
    else:
        raise LispSyntaxError(ast)

def _macro(ast, env):
    (_, params, body) = ast
    return Macro(params, body)

def _expand_1(ast, env):
    # def transform(ast, substitutions):
    #     if is_symbol(ast) and ast in substitutions:
    #         return substitutions[ast]
    #     elif is_list(ast):
    #         return [transform(x, substitutions) for x in ast]
    #     else:
    #         return ast
    
    def _is_macro_type(ast, env):
        if is_list(ast): 
            return False
        else: 
            return is_macro(ast) \
                or is_macro(env.get(ast, False))

    # extract form to expand
    form = evaluate(ast[1], env)
    if not _is_macro_type(form[0], env):
        # if form is not a macro call, return form directly
        return form

    macro = evaluate(form[0], env)
    substitutions = Environment(zip(macro.params, form[1:]), env)
    return evaluate(macro.body, substitutions)

def _expand(ast, env):
    return "not implemented"

def _cond(ast, env):
    for predicate, ast in ast[1:]:
        p = evaluate(predicate, env)
        _assert_boolean(p, predicate)
        if value_of(p) is True:
            return evaluate(ast, env)

def _if(ast, env):
    _assert_exp_length(ast, 4)
    (_, pred, then_exp, else_exp) = ast
    p = evaluate(pred, env)
    _assert_boolean(p, pred)
    return evaluate((then_exp if value_of(p) else else_exp), env)

def _atom(ast, env):
    arg = evaluate(ast[1], env)
    return boolean(is_atom(arg))

def _eval(ast, env):
    _assert_exp_length(ast, 2)
    (_, exp) = ast
    return evaluate(evaluate(exp, env), env)

def _define(ast, env):
    _assert_valid_definition(ast[1:])
    env[ast[1]] = evaluate(ast[2], env)

def _lambda(ast, env):
    _assert_exp_length(ast, 3)
    (_, params, body) = ast
    return Lambda(params, body, env)

def _begin(ast, env):
    if len(ast[1:]) == 0:
        raise LispSyntaxError("begin cannot be empty: %s" % unparse(ast))
    results = [evaluate(exp, env) for exp in ast[1:]]
    return results[-1]

def _quote(ast, env):
    def quasiquote(ast, env):
        if not isinstance(ast, list):
            return ast
        elif ast[0] == "unquote":
            _assert_exp_length(ast, 2)
            return evaluate(ast[1], env)
        else:
            return [quasiquote(exp, env) for exp in ast]

    _assert_exp_length(ast, 2)
    if ast[0] == 'quote':
        return ast[1]
    elif ast[0] == 'quasiquote':
        return quasiquote(ast[1], env)
    elif ast[0] == 'unquote':
        raise LispSyntaxError("Unquote outside of quasiquote: %s" % unparse(ast))

def _set(ast, env):
    _assert_exp_length(ast, 3)
    (_, var, exp) = ast
    env.defining_env(var)[var] = evaluate(exp, env)

def _let(ast, env):
    _assert_exp_length(ast, 3)
    for d in ast[1]:
        _assert_valid_definition(d)
    defs = [(d[0], evaluate(d[1], env)) for d in ast[1]]
    return evaluate(ast[2], Environment(defs, env))

def _apply(ast, env):
    cls = evaluate(ast[0], env)

    if not is_closure(cls):
        raise LispTypeError("Call to non-function: " + unparse(ast))

    args = [evaluate(exp, env) for exp in ast[1:]]
    if is_lambda(cls):
        if len(args) != len(cls.params):
            msg = "Wrong number of arguments, expected %d got %d: %s" \
                % (len(cls.params), len(args), unparse(ast))
            raise LispTypeError(msg)
        return evaluate(cls.body, Environment(zip(cls.params, args), env))
    elif is_builtin(cls):
        return cls.fn(*args)
    else:
        raise Exception("Unknown implementation of Closure: %s" % cls)

## Syntax assertions

def _assert_exp_length(ast, length):
    if len(ast) > length:
        msg = "Malformed %s, too many arguments: %s" % (ast[0], unparse(ast))
        raise LispSyntaxError(msg)
    elif len(ast) < length:
        msg = "Malformed %s, too few arguments: %s" % (ast[0], unparse(ast))
        raise LispSyntaxError(msg)

def _assert_valid_definition(d):
    if len(d) != 2:
        msg = "Wrong number of arguments for variable definition: %s" % d
        raise LispSyntaxError(msg)
    elif not isinstance(d[0], str):
        msg = "Attempted to define non-symbol as variable: %s" % d
        raise LispSyntaxError(msg)

def _assert_boolean(p, exp=None):
    if not is_boolean(p):
        msg = "Boolean required, got '%s'. " % unparse(p)
        if exp is not None:
            msg += "Offending expression: %s" % unparse(exp)
        raise LispTypeError(msg)
