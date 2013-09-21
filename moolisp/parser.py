# -*- coding: utf-8 -*-

import re

from errors import LispSyntaxError

def unparse(ast):
    if isinstance(ast, bool):
        return "#t" if ast else "#f"
    elif isinstance(ast, list):
        if ast[0] == "quote":
            return "'%s" % unparse(ast[1])
        else:
            return "(%s)" % " ".join([unparse(x) for x in ast])
    else:
        # string, integer or Closure
        return str(ast)

def parse(source):
    "Creates an Abstract Syntax Tree (AST) from program source (as string)"
    source = remove_comments(source)
    source = expand_quote_ticks(source)
    return analyze(tokenize(source))

def remove_comments(source):
    return re.sub(r";.*\n", "\n", source)

def expand_quote_ticks(source):
    while re.search(r"'", source):
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
