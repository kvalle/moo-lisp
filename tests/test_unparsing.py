# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from moolisp.types import Lambda, Builtin
from moolisp.env import Environment
from moolisp.parser import unparse

class TestUnparsing:

    def test_unparse_boolean(self):
        assert_equals("#t", unparse(True))
        assert_equals("#f", unparse(False))

    def test_unparse_symbol(self):
        assert_equals("foo", unparse("foo"))

    def test_unparse_number(self):
        assert_equals("42", unparse(42))

    def test_unparse_list(self):
        assert_equals("(1 2 3)", unparse([1, 2, 3]))

    def test_unparse_nested_lists(self):
        lst = [["foo", 2], True, [1, [2, 3], False]]
        assert_equals("((foo 2) #t (1 (2 3) #f))", unparse(lst))

    def test_unparse_lambda(self):
        fn = Lambda(["x", "y"], ["+", "x", "y"], Environment())
        assert_equals("<lambda/2>", unparse(fn))

    def test_unparse_builtin(self):
        assert_equals("<builtin/2>", unparse(Builtin(lambda a, b: 42)))
        assert_equals("<builtin/0+>", unparse(Builtin(lambda *args: 42)))
        assert_equals("<builtin/1+>", unparse(Builtin(lambda a, *rest: 42)))

    def test_uparse_quote_symbol(self):
        assert_equals("'foo", unparse(["quote", "foo"]))
        assert_equals("''foo", unparse(["quote", ["quote", "foo"]]))
        assert_equals("'''foo", unparse(["quote", ["quote", ["quote", "foo"]]]))

    def test_unparse_quote_list(self):
        assert_equals("'(1 2 3)", unparse(["quote", [1, 2, 3]]))
        assert_equals("''(1 2 3)", unparse(["quote", ["quote", [1, 2, 3]]]))
