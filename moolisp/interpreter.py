# -*- coding: utf-8 -*-

import re
from errors import LispSyntaxError, LispTypeError
from env import Environment, get_default_env
from types import Closure, Lambda, Builtin 

def unparse(ast):
    if isinstance(ast, list):
        return "(%s)" % " ".join([unparse(x) for x in ast])
    elif isinstance(ast, bool):
        return "#t" if ast else "#f"
    else:
        return str(ast)

def parse(source):
    "Creates an Abstract Syntax Tree (AST) from program source (as string)"
    return analyze(tokenize(preprocess(source)))

def preprocess(source):
    "Preprocessing steps such as removing comments (string -> string)"
    # remove comments
    source = re.sub(r";.*\n", "\n", source)  
    # 'foo -> (quote foo)
    source = re.sub(r"'([^\s\(\)]+)", r"(quote \1)", source)  
    # '(foo bar lol) -> (quote (foo bar lol))
    source = re.sub(r"'\((.*)\)", r"(quote (\1))", source)  
    return source

def tokenize(source):
    "Create list of tokens from (preprocessed) program source"
    source = source.replace("(", " ( ").replace(")", " ) ")
    return source.split()

def analyze(tokens):
    """Transform list of token to AST

    Expects the tokens to constitute *one* single full AST.
    Throws an error otherwise.
    """
    sexp, rest = _read_elem(tokens)
    if len(rest) > 0:
        raise LispSyntaxError("Expected EOF got %s" % unparse(rest))
    return sexp

def _read_elem(tokens):
    if len(tokens) == 0:
        raise LispSyntaxError("Unexpected EOF")
    if tokens[0] == "(":
        return _read_list(tokens[1:])
    else:
        atom = _atomize(tokens[0])
        return (atom, tokens[1:])

def _read_list(tokens):
    res = []
    while True:
        el, tokens = _read_elem(tokens)
        if el == ")": 
            break
        res.append(el)
    return res, tokens

def _atomize(elem):
    if elem == "#f":
        return False
    elif elem == "#t":
        return True
    elif elem.isdigit():
        return int(elem)
    else: 
        return elem  # symbols or lists

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

def interpret(source, env=None):
    """Interpret a moo-lisp program statement."""
    if env is None:
        env = get_default_env()
    return evaluate(parse(source), env)
