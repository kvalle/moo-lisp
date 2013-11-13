# -*- coding: utf-8 -*-

from errors import LispSyntaxError, LispTypeError
from env import Environment
from types import Lambda, Macro
from types import value_of, boolean, is_boolean, is_atom, is_symbol, is_list
from types import is_macro, is_lambda, is_builtin
from parser import unparse

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_symbol(ast): return env[ast]
    elif is_atom(ast): return ast
    elif is_list(ast):
        if ast[0] == 'macro': return eval_macro(ast, env)
        elif ast[0] == 'expand': return eval_expand(ast, env)
        elif ast[0] == 'expand-1': return eval_expand_1(ast, env)
        elif ast[0] == 'cond': return eval_cond(ast, env)
        elif ast[0] == 'let': return eval_let(ast, env)
        elif ast[0] == 'eval': return eval_eval(ast, env)
        elif ast[0] == 'set!': return eval_set(ast, env)
        elif ast[0] == 'quote': return eval_quote(ast, env)
        elif ast[0] == 'quasiquote': return eval_quasiquote(ast, env)
        elif ast[0] in ('lambda', 'λ'): return eval_lambda(ast, env)
        elif ast[0] == 'atom': return eval_atom(ast, env)
        elif ast[0] == 'begin': return eval_begin(ast, env)
        elif ast[0] == 'define': return eval_define(ast, env)
        else: 
            fn = evaluate(ast[0], env)
            if is_macro(fn): 
                return apply_macro(ast, env)
            elif is_lambda(fn): 
                return apply_lambda(ast, env)
            elif is_builtin(fn): 
                return apply_builtin(ast, env)
            else: 
                raise LispTypeError("Call to: " + unparse(ast[0]))
    else:
        raise LispSyntaxError(ast)

def apply_macro(ast, env):
    expanded_form = expand_once(ast, env)
    return evaluate(expanded_form, env)

def apply_lambda(ast, env):
    fn = evaluate(ast[0], env)
    args = ast[1:]

    if len(args) != len(fn.params):
        msg = "Wrong number of arguments, expected %d got %d: %s" \
            % (len(fn.params), len(args), unparse(ast))
        raise LispTypeError(msg)
    
    args = [evaluate(exp, env) for exp in ast[1:]]
    return evaluate(fn.body, Environment(zip(fn.params, args), env))

def apply_builtin(ast, env):
    fn = evaluate(ast[0], env)
    args = [evaluate(exp, env) for exp in ast[1:]]
    return fn.fn(*args)

def eval_macro(ast, env):
    (_, params, body) = ast
    return Macro(params, body)

def expand_once(form, env):
    """expand macro form once

    Assumes first element of form is a macro or macro call.
    Evaluates this element in case it is a reference"""

    # might be call to named macro in the environment
    macro = evaluate(form[0], env) 
    
    # expand
    substitutions = Environment(zip(macro.params, form[1:]), env)
    return evaluate(macro.body, substitutions)

def _is_macro_call(ast, env):
    first = ast[0]
    return is_macro(first) \
        or is_macro(env.get(first, False))

def eval_expand_1(ast, env):
    form = evaluate(ast[1], env)
    if _is_macro_call(form, env):
        form = expand_once(form, env)
    return form

def eval_expand(ast, env):
    form = evaluate(ast[1], env)
    while _is_macro_call(form, env):
        form = expand_once(form, env)
    return form

def eval_cond(ast, env):
    for predicate, ast in ast[1:]:
        p = evaluate(predicate, env)
        _assert_boolean(p, predicate)
        if value_of(p) is True:
            return evaluate(ast, env)

def eval_atom(ast, env):
    arg = evaluate(ast[1], env)
    return boolean(is_atom(arg))

def eval_eval(ast, env):
    _assert_exp_length(ast, 2)
    (_, exp) = ast
    return evaluate(evaluate(exp, env), env)

def eval_define(ast, env):
    _assert_valid_definition(ast[1:])
    env[ast[1]] = evaluate(ast[2], env)
    return ast[1]

def eval_lambda(ast, env):
    _assert_exp_length(ast, 3)
    (_, params, body) = ast
    return Lambda(params, body, env)

def eval_begin(ast, env):
    if len(ast[1:]) == 0:
        raise LispSyntaxError("begin cannot be empty: %s" % unparse(ast))
    results = [evaluate(exp, env) for exp in ast[1:]]
    return results[-1]

def eval_quasiquote(ast, env):
    def qq(ast, env):
        if not isinstance(ast, list):
            return ast
        elif ast[0] == "unquote":
            _assert_exp_length(ast, 2)
            return evaluate(ast[1], env)
        else:
            return [qq(exp, env) for exp in ast]

    _assert_exp_length(ast, 2)    
    return qq(ast[1], env)

def eval_quote(ast, env):
    _assert_exp_length(ast, 2)
    return ast[1]

def eval_set(ast, env):
    _assert_exp_length(ast, 3)
    (_, var, exp) = ast
    env.defining_env(var)[var] = evaluate(exp, env)

def eval_let(ast, env):
    _assert_exp_length(ast, 3)
    for d in ast[1]:
        _assert_valid_definition(d)
    defs = [(d[0], evaluate(d[1], env)) for d in ast[1]]
    return evaluate(ast[2], Environment(defs, env))

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
