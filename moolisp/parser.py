# -*- coding: utf-8 -*-

import re
from errors import LispSyntaxError

quote_names = {
    'quote': "'",
    'quasiquote': "`",
    'unquote': ","
}
quote_ticks = dict((tick, name) for name, tick in quote_names.iteritems())

def unparse(ast):
    if isinstance(ast, bool):
        return "#t" if ast else "#f"
    elif isinstance(ast, list):
        if len(ast) > 0 and ast[0] in quote_names:
            return "%s%s" % (quote_names[ast[0]], unparse(ast[1]))
        else:
            return "(%s)" % " ".join([unparse(x) for x in ast])
    else:
        return str(ast)  # string, integer or Closure

def parse(source):
    """Parse string representation of one single expression
    into the corresponding Abstract Syntax Tree"""
    source = remove_comments(source)
    exp, rest = partition_exp(source)
    if rest:
        raise LispSyntaxError('Expected EOF')
    elif exp[0] in quote_ticks:
        return [quote_ticks[exp[0]], parse(exp[1:])]
    elif exp[0] == "(":
        end = find_matching_paren(exp)
        return [parse(e) for e in split_exps(exp[1:end])]
    else:
        return atomize(exp)

def atomize(elem):
    if elem == "#f":
        return False
    elif elem == "#t":
        return True
    elif elem.isdigit():
        return int(elem)
    else: 
        return elem  # symbols or lists

def parse_multiple(source):
    """Creates a list of ASTs from program source 
    constituting multiple expressions"""
    return [parse(exp) for exp in split_exps(source)]

def split_exps(source):
    """Splits a source string into subexpressions 
    that can be parsed individually"""
    rest = source.strip()
    exps = []
    while rest:
        exp, rest = partition_exp(rest)
        exps.append(exp)
    return exps

def partition_exp(source):
    """Split string into (exp, rest) where exp is the 
    first expression in the string and rest is the 
    rest of the string after this expression."""
    source = source.strip()
    if source[0] in quote_ticks:
        exp, rest = partition_exp(source[1:])
        return source[0] + exp, rest
    elif source[0] == "(":
        last = find_matching_paren(source)
        return source[:last + 1], source[last + 1:]
    else:
        match = re.match(r"^[^\s)']+", source)
        end = match.end()
        atom = source[:end]
        return atom, source[end:]

def find_matching_paren(source, start=0):
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

def remove_comments(source):
    return re.sub(r";.*\n", "\n", source)
