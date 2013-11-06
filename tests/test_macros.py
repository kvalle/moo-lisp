# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_true, assert_false, assert_is_instance

from moolisp import interpret
from moolisp.evaluator import evaluate
from moolisp.env import Environment, get_default_env
from moolisp.types import Macro, boolean, integer, is_macro

class TestMacros:

    def test_defining_macro(self):
        """(macro ...) should return something of type macro"""

        macro = evaluate(["macro", ["foo", "bar"], ["quote", ["bar", "foo"]]], Environment())
        assert_true(is_macro(macro))
        assert_equals(["foo", "bar"], macro.params)
        assert_equals(["quote", ["bar", "foo"]], macro.body)

    def test_expand_1_on_non_macro_returns_unchanged(self):
        """expand-1, when called with a form that is not a macro call, 
        should return that form"""

        assert_equals("42", interpret("(expand-1 '42)", Environment()))

    def test_expand_simple_macro_once(self):
        """expand-1 should expand macro call expression once"""
        env = get_default_env()
        interpret("""(define swp 
                        (macro (foo bar) 
                            (list bar foo)))""", env)
        assert_equals("(42 #t)", interpret("(expand-1 '(swp #t 42))", env))

    def test_expand_1_only_expands_once(self):
        """when used on recursive macro, expand-1 only expands once"""

        env = Environment()
        interpret("""(define add-foo 
                        (macro (lst) 
                            `(add-foo (cons foo ,lst))))""", env)
        assert_equals("(add-foo (cons foo nil))", 
            interpret("(expand-1 '(add-foo nil))", env))        

    def test_expand_1_used_twice(self):
        """expand-1 used twice expands macro twice

        example from clojure:
        
            user=> (defmacro add-foo [lst] `(add-foo (cons foo ~lst)))
            #'user/add-foo
            user=> (macroexpand-1 '(add-foo nil))
            (user/add-foo (clojure.core/cons user/foo nil))
            user=> (macroexpand-1 (macroexpand-1 '(add-foo nil)))
            (user/add-foo (clojure.core/cons user/foo (clojure.core/cons user/foo nil)))
        """

        env = Environment()
        interpret("""(define add-foo 
                        (macro (lst) 
                            `(add-foo (cons foo ,lst))))""", env)
        assert_equals("(add-foo (cons foo (cons foo nil)))", 
            interpret("(expand-1 (expand-1 '(add-foo nil)))", env))        
