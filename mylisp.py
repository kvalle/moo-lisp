class LispSyntaxError(SyntaxError): 
    pass
class LispNamingError(LookupError): 
    pass

def to_string(ast):
    if isinstance(ast, list):
        return "(%s)" % " ".join([to_string(x) for x in ast])
    elif isinstance(ast, bool):
        return "#t" if ast else "#f"
    else:
        return str(ast)

##
## Parsing
##

def parse(source):
    return analyze(tokenize(source))

def tokenize(source):
    return source.replace("(", " ( ").replace(")", " ) ").split()

def analyze(tokens):
    sexp, rest = read_elem(tokens)
    if len(rest) > 0:
        raise LispSyntaxError("Expected EOF got '%s'" % to_string(rest))
    return sexp

def read_elem(tokens):
    if len(tokens) == 0:
        raise LispSyntaxError("Unexpected EOF")
    if tokens[0] == "(":
        return read_list(tokens[1:])
    else:
        atom = atomize(tokens[0])
        return (atom, tokens[1:])

def read_list(tokens):
    res = []
    while True:
        el, tokens = read_elem(tokens)
        if el == ")": 
            break
        res.append(el)
    return res, tokens

def atomize(elem):
    if elem == "#f":
        return False
    elif elem == "#t":
        return True
    elif elem.isdigit():
        return int(elem)
    else: 
        return elem  # symbols or lists

##
## Evaluating
##

def evaluate(ast, env={}):
    if isinstance(ast, str):
        try:
            return env[ast]
        except KeyError:
            raise LispNamingError("Variable '%s' is undefined" % ast)
    elif not isinstance(ast, list):
        return ast
    elif ast[0] == 'if': 
        assert_exp_length(ast, 4, "if")
        (_, pred, then_exp, else_exp) = ast
        return evaluate((then_exp if evaluate(pred, env) else else_exp), env)
    elif ast[0] == 'define': 
        assert_exp_length(ast, 3, "define")
        (_, variable, expression) = ast
        env[variable] = evaluate(expression, env)
    else:
        raise Exception("something is missing")

def assert_exp_length(ast, length, name):
    if len(ast) != length:
        raise LispSyntaxError("Malformed %s: %s" % (name, to_string(ast)))

##
## Lisp interpreter
##

class Lisp:
    def interpret(self, source):
        raise NotImplementedError
