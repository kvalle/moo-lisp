# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from moolisp.types import boolean, integer
from moolisp.parser import unparse

class TestUnparsing:
    """Suite for testing the `unparse` function, which takes an 
    Abstract Syntax Tree (AST) and produces Moo lisp syntax"""

    def test_unparse_bool(self):
        assert_equals("#t", unparse(boolean(True)))
        assert_equals("#f", unparse(boolean(False)))

    def test_unparse_int(self):
        assert_equals("1", unparse(integer(1)))
        assert_equals("1337", unparse(integer(1337)))
        assert_equals("-42", unparse(integer(-42)))

    def test_unparse_symbol(self):
        assert_equals("+", unparse("+"))
        assert_equals("foo", unparse("foo"))
        assert_equals("lambda", unparse("lambda"))

    def test_unparse_list(self):
        assert_equals("(1 2 3)", unparse([integer(1), integer(2), integer(3)]))
        assert_equals("(if #t 42 #f)", \
            unparse(["if", boolean(True), integer(42), boolean(False)]))

    def test_unparse_quotes(self):
        assert_equals("'foo", unparse(["quote", "foo"]))
        assert_equals("'(1 2 3)", unparse(["quote", [integer(1), integer(2), integer(3)]]))

    def test_unparse_quasiquotes_with_unquote(self):
        ast = ["quote", ["quasiquote", ["foo", ["unquote", "bar"]]]]
        assert_equals("'`(foo ,bar)", unparse(ast))

    def test_unparse_empty_list(self):
        assert_equals("()", unparse([]))
