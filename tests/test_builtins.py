# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from moolisp.types import integer, true, false
from moolisp import interpret
from moolisp.env import get_default_env

class TestBuiltins:

    def setup(self):
        self.env = get_default_env()

    def test_arithmetic_functions(self):
        """Sanity check for the builtin artihmetic functions"""

        assert_equals("5", interpret('(+ 2 3)', self.env))
        assert_equals("3", interpret('(- 5 2)', self.env))
        assert_equals("8", interpret('(* 4 2)', self.env))
        assert_equals("8", interpret('(/ 16 2)', self.env))
        assert_equals("1", interpret('(mod 5 2)', self.env))

    def test_comparator_functions(self):
        """Sanity check for the builtin comparators"""

        assert_equals("#f", interpret('(= 2 3)', self.env))
        assert_equals("#t", interpret('(= #t #t)', self.env))
        assert_equals("#f", interpret('(> 1 2)', self.env))
        assert_equals("#t", interpret('(> 2 1)', self.env))
        assert_equals("#t", interpret('(< 1 2)', self.env))
        assert_equals("#f", interpret('(< 2 1)', self.env))
        assert_equals("#t", interpret('(>= 2 1)', self.env))
        assert_equals("#t", interpret('(>= 2 2)', self.env))
        assert_equals("#f", interpret('(>= 2 3)', self.env))
        assert_equals("#f", interpret('(<= 2 1)', self.env))
        assert_equals("#t", interpret('(<= 2 2)', self.env))
        assert_equals("#t", interpret('(<= 2 3)', self.env))

    def test_list_nil(self):
        """Test the predefined nil value"""

        assert_equals(interpret("(quote ())", self.env), interpret("nil", self.env))
        assert_equals("()", interpret("nil", self.env))

    def test_creating_lists(self):
        """Test different ways to create lists"""

        xs = "(1 2 #t 4)"
        assert_equals(xs, interpret("(quote (1 2 #t 4))", self.env))
        assert_equals(xs, interpret("(cons 1 (cons 2 (cons #t (cons 4 nil))))", self.env))
        assert_equals(xs, interpret("(list 1 2 #t 4)", self.env))

    def test_deconstruction_of_lists(self):
        """Tests picking elements from lists using car and cdr"""

        interpret("(define lst (list 1 2 3 4 5))", self.env)
        assert_equals("1", interpret("(car lst)", self.env))
        assert_equals("2", interpret("(car (cdr lst))", self.env))
        assert_equals("(3 4 5)", interpret("(cdr (cdr lst))", self.env))
