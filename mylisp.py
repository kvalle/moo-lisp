#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cmd, sys

class LispError(Exception): 
    pass
class LispSyntaxError(SyntaxError, LispError): 
    pass
class LispNamingError(LookupError, LispError): 
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
## Environment
##

class Environment(dict):
    def __init__(self, vars=None, outer=None):
        self.outer = outer
        if vars:
            self.update(vars)

    def __getitem__(self, key):
        return self.defining_env(key).get(key)

    def defining_env(self, variable):
        "Find the innermost environment defining a variable"
        if variable in self:
            return self
        elif self.outer is not None:
            return self.outer.defining_env(variable)
        else:
            raise LispNamingError("Variable '%s' is undefined" % variable)

##
## Evaluating
##

default_environment = Environment()

def evaluate(ast, env=default_environment):
    if isinstance(ast, str):
        return env[ast]
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
    elif ast[0] == 'lambda':
        assert_exp_length(ast, 3, "lambda")
        (_, params, body) = ast
        return lambda *args: evaluate(body, Environment(zip(params, args), env))
    else:
        fn = evaluate(ast[0], env)
        args = [evaluate(exp, env) for exp in ast[1:]]
        return fn(*args)

def assert_exp_length(ast, length, name):
    if len(ast) != length:
        raise LispSyntaxError("Malformed %s: %s" % (name, to_string(ast)))

##
## Lisp interpreter
##

class Lisp:
    def interpret(self, source):
        raise NotImplementedError

##
## Main
##

class REPL(cmd.Cmd, object):

    env = default_environment
    prompt = "→ "

    def emptyline(self):
        pass

    def default(self, line):
        "Handle parsing of LISPy inputs"
        try:
            result = evaluate(parse(line), self.env)
            if result is not None: 
                print to_string(result)
        except LispError, e:
            print "! %s" % e

    def do_EOF(self, s):
        "Exit REPL on ^D"
        return True

    def do_help(self, s):
        print "This is the help/usage/documentation."
        print "It's not quite written yet."

    def preloop(self):
        print "Hey-ho, welcome to the REPL!"
        super(REPL, self).preloop()

    def postloop(self):
        print '\nSo long!'
        super(REPL, self).postloop()

if __name__ == '__main__':
    repl = REPL()
    if sys.argv[1]:
        for line in open(sys.argv[1], 'r'):
            repl.onecmd(line)
    else:
        repl.cmdloop()
