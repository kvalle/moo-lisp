# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from moolisp.interpreter import interpret, default_env

class TestDefaultEnvironment:

    ## nil

    def test_list_nil(self):
        """Test the predefined nil value"""

        assert_equals(interpret("(quote ())"), interpret("nil"))
        assert_equals("()", interpret("nil"))

    ## if macro

    def test_simple_if_statement(self):
        assert_equals("42", interpret("(if #t 42 1000)"))

    def test_if_with_variable_lookup(self):
        """Test evaluation of expressions (variable lookup) within if form"""

        env = default_env()
        interpret("(define pred #f)", env)
        interpret("(define else 42)", env)
        assert_equals("42", interpret("(if pred then else)", env))

    def test_if_expands_to_cond_statement(self):
        """Test the expansion of an if statement into the corresponding cond"""

        assert_equals("(cond (#t 42) (#t 100))",
            interpret("(expand-1 '(if #t 42 100))"))
