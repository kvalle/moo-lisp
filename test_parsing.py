from nose.tools import assert_equals, assert_raises_regexp

import mylisp
from mylisp import tokenize, parse
from mylisp import LispSyntaxError

class TestParsing:

    def setup(self):
        self.lisp = mylisp.Lisp()

    def test_tokenize_single_atom(self):
        assert_equals(["foo"], tokenize("foo"))

    def test_tokenize_list(self):
        source = "(foo 1 2)"
        tokens = ["(", "foo", "1", "2", ")"]
        assert_equals(tokens, tokenize(source))

    def test_parse_on_simple_list(self):
        program = "(foo bar)"
        assert_equals(["foo", "bar"], parse(program))

    def test_parse_on_tested_list(self):
        program = "(foo (bar x y) (baz x))"
        ast = ["foo", 
                ["bar", "x", "y"], 
                ["baz", "x"]]
        assert_equals(ast, parse(program))

    def test_parse_exception_missing_paren(self):
        with assert_raises_regexp(LispSyntaxError, "Unexpected EOF"):
            parse("(foo (bar x y)")

    def test_parse_exception_extra_paren(self):
        with assert_raises_regexp(LispSyntaxError, "Expected EOF"):
            parse("(foo (bar x y)))")
