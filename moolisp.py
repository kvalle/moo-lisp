#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cmd
import sys
import re
import os

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
    source = re.sub(r";.*\n", "\n", source)
    source = source.replace("(", " ( ").replace(")", " ) ")
    return source.split()

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

def evaluate(ast, env):
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
    elif ast[0] == 'begin':
        if len(ast[1:]) == 0:
            raise LispSyntaxError("begin cannot be empty: %s" % to_string(ast))
        results = [evaluate(exp, env) for exp in ast[1:]]
        return results[-1]
    else:
        fn = evaluate(ast[0], env)
        args = [evaluate(exp, env) for exp in ast[1:]]
        return fn(*args)

def assert_exp_length(ast, length, name):
    if len(ast) != length:
        raise LispSyntaxError("Malformed %s: %s" % (name, to_string(ast)))

##
## Interpreter
##

import operator as op

default_environment = Environment({
    "*": op.mul, "-": op.sub, "+": op.add, "/": op.div,
    '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq, 'not': op.not_
})

def interpret(source, env=default_environment):
    return evaluate(parse(source), env)

##
## REPL
##

ATTRIBUTES = {
    'bold': 1, 
    'dark': 2
}

COLORS = {
    'grey': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}

def colored(text, color, attr=None):
    if os.getenv('ANSI_COLORS_DISABLED'):
        return text

    format = '\033[%dm'

    color = format % COLORS[color]
    attr = format % ATTRIBUTES[attr] if attr is not None else ""
    reset = '\033[0m'

    return color + attr + text + reset

def grey(text):
    return colored(text, "grey", attr='bold')

class REPL(cmd.Cmd, object):

    prompt = colored("→  ", "grey")

    def emptyline(self):
        pass

    def default(self, line):
        "Handle parsing of LISPy inputs"
        try:
            result = interpret(line)
            if result is not None: 
                print to_string(result)
        except LispError, e:
            print colored("! ", "red") + str(e)

    def do_EOF(self, s):
        "Exit REPL on ^D"
        return True

    def do_help(self, s):
        with open("README.txt", "r") as f:
            for line in f:
                print line,

    def preloop(self):
        print
        print "                       " + grey("    ^__^             ")
        print "          welcome to   " + grey("    (oo)\_______     ")
        print "         the MOO-lisp  " + grey("    (__)\       )\/\ ")
        print "             REPL      " + grey("        ||----w |    ")
        print "                       " + grey("        ||     ||    ")
        print
        super(REPL, self).preloop()

    def postloop(self):
        print '\nBye :)'
        super(REPL, self).postloop()

if __name__ == '__main__':
    repl = REPL()
    if len(sys.argv) > 1:
        for line in open(sys.argv[1], 'r'):
            repl.onecmd(line)
    else:
        repl.cmdloop()