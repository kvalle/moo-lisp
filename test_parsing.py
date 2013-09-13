from unittest.case import SkipTest
from nose.tools import eq_

import mylisp
from mylisp import tokenize, parse

class TestParsing:

    def setup(self):
        self.lisp = mylisp.Lisp()

    def test_tokenize_single_atom(self):
        eq_(["foo"], tokenize("foo"))

    def test_tokenize_list(self):
        source = "(foo 1 2)"
        tokens = ["(", "foo", "1", "2", ")"]
        eq_(tokens, tokenize(source))

    def test_parse_on_simple_list(self):
        program = "(foo bar)"
        eq_(["foo", "bar"], parse(program))

    def test_parse_on_tested_list(self):
        program = "(foo (bar x y) (baz x))"
        ast = ["foo", ["bar", "x", "y"], ["baz", "x"]]
        eq_(ast, parse(program))