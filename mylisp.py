def parse(source):
    return analyze(tokenize(source))

def tokenize(source):
    return source.replace("(", " ( ").replace(")", " ) ").split()

def analyze(tokens):
    return atomize(treeify(tokens))

def treeify(tokens):
    exp, _ = read_elem(tokens)
    return exp

def read_elem(tokens):
    if tokens[0] == "(":
        return read_list(tokens[1:])
    else:
        return (tokens[0], tokens[1:])

def read_list(tokens):
    res = []
    while True:
        el, tokens = read_elem(tokens)
        if el == ")": break
        res.append(el)
    return res, tokens

def atomize(ast):
    "TODO"
    return ast

class Lisp:
    def interpret(self, source):
        raise NotImplementedError
