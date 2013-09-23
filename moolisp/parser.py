# -*- coding: utf-8 -*-

import re

from errors import LispSyntaxError

quotes = {
    "'": 'quote',
    "`": 'quasiquote',
    ",": 'unquote'
}
ticks = {quote: tick for tick, quote in quotes.items()}
quote_ticks = "".join(quotes.keys())

def unparse(ast):
    if isinstance(ast, bool):
        return "#t" if ast else "#f"
    elif ast == []:
        return "()"
    elif isinstance(ast, list):
        if ast[0] in ticks:
            return "%s%s" % (ticks[ast[0]], unparse(ast[1]))
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

def expand_quoted_symbol(source):
    # match anything with a tick (`',) followed by at least one character
    # that is not whitespace, a paren or another tick
    regex = r"([%(ticks)s])([^%(ticks)s\(\s]+)" % {"ticks": quote_ticks}
    match = re.search(regex, source)
    if match:
        start, end = match.span()
        source = "%(pre)s(%(quote)s %(quoted)s)%(post)s" % {
            "pre": source[:start], 
            "quote": quotes[match.group(1)], 
            "quoted": match.group(2), 
            "post": source[end:]
        }
    return source

def expand_quoted_list(source):
    # match any tick followed directly by an opening parenthesis
    regex = r"([%(ticks)s])\(" % {"ticks": quote_ticks}
    match = re.search(regex, source)
    if match:
        start = match.start()
        end = find_matching_paren(source, start + 1)
        source = "%(pre)s(%(quote)s %(quoted)s)%(post)s" % {
            "pre": source[:start],
            "quote": quotes[match.group(1)],
            "quoted": source[start + 1:end],
            "post": source[end:] 
        }
    return source

def expand_quote_ticks(source):
    while re.search(r"[%s]" % quote_ticks, source):
        source = expand_quoted_symbol(source)
        source = expand_quoted_list(source)
    return source

def find_matching_paren(source, start):
    """Given a string and the index of an opening parenthesis, determine 
    the index of the matching closing paren"""

    assert source[start] == '('
    pos = start
    open_brackets = 1
    while open_brackets > 0:
        pos += 1
        if len(source) == pos:
            raise LispSyntaxError("Unbalanced expression: %s" % source[start:])
        if source[pos] == '(':
            open_brackets += 1
        if source[pos] == ')':
            open_brackets -= 1
    return pos

def tokenize(source):
    "Create list of tokens from (preprocessed) program source"
    return source.replace("(", " ( ").replace(")", " ) ").split()

def untokenize(tokens):
    return " ".join(tokens).replace("( ", "(").replace(" )", ")")

def analyze(tokens):
    """Transform list of token to AST

    Expects the tokens to constitute *one* single full AST.
    Throws an error otherwise.
    """
    sexp, rest = _read_elem(tokens)
    if len(rest) > 0:
        raise LispSyntaxError("Expected EOF got '%s'" % untokenize(rest))
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
