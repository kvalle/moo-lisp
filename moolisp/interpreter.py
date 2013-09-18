# -*- coding: utf-8 -*-

import re
from errors import LispSyntaxError, LispTypeError
from env import Environment

class Closure:
    def __init__(self, fn, env):
        self.fn = fn
        self.env = env

def to_string(ast):
    if isinstance(ast, list):
        return "(%s)" % " ".join([to_string(x) for x in ast])
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
    source = re.sub(r"'([\w]+)", r"(quote \1)", source)  
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
        raise LispSyntaxError("Expected EOF got %s" % to_string(rest))
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
        _assert_exp_length(ast, 4, "if")
        (_, pred, then_exp, else_exp) = ast
        return evaluate((then_exp if evaluate(pred, env) else else_exp), env)
    elif ast[0] == 'define': 
        _assert_exp_length(ast, 3, "define")
        (_, variable, expression) = ast
        env[variable] = evaluate(expression, env)
    elif ast[0] == 'lambda' or ast[0] == 'λ':
        _assert_exp_length(ast, 3, "lambda")
        (_, params, body) = ast
        fn = {"params": params, "body": body}
        return Closure(fn, env)
    elif ast[0] == 'begin':
        if len(ast[1:]) == 0:
            raise LispSyntaxError("begin cannot be empty: %s" % to_string(ast))
        results = [evaluate(exp, env) for exp in ast[1:]]
        return results[-1]
    elif ast[0] == 'quote':
        _assert_exp_length(ast, 2, "quote")
        (_, exp) = ast
        return exp
    elif ast[0] == 'set!':
        _assert_exp_length(ast, 3, "set!")
        (_, var, exp) = ast
        env.defining_env(var)[var] = evaluate(exp, env)
    elif ast[0] == "-": 
        return evaluate(ast[1], env) - evaluate(ast[2], env)
    elif ast[0] == "*": 
        return evaluate(ast[1], env) * evaluate(ast[2], env)
    elif ast[0] == "<=": 
        return evaluate(ast[1], env) <= evaluate(ast[2], env)
    else:
        cls = evaluate(ast[0], env)
        if not isinstance(cls, Closure):
            raise LispTypeError("Call to non-function: " + to_string(ast))
        args = [evaluate(exp, env) for exp in ast[1:]]
        params = cls.fn["params"]
        if not len(args) == len(params):
            msg = "Wrong number of arguments, expected %d got %d: %s" \
                % (len(params), len(args), to_string(ast))
            raise LispTypeError(msg)
        return evaluate(cls.fn["body"], Environment(zip(params, args), env))

def _assert_exp_length(ast, length, name):
    if len(ast) > length:
        msg = "Malformed %s, too many arguments: %s" % (name, to_string(ast))
        raise LispSyntaxError(msg)
    elif len(ast) < length:
        msg = "Malformed %s, too few arguments: %s" % (name, to_string(ast))
        raise LispSyntaxError(msg)

def interpret(source, env=None):
    """Interpret a moo-lisp program statement."""
    if env is None:
        env = Environment()
    return evaluate(parse(source), env)
