# -*- coding: utf-8 -*-

"""
Tests for the macro system of Moo Lisp.
The macros are heavily inspired by how Clojure macros works.
"""

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_true, assert_false, assert_is_instance

from moolisp import interpret
from moolisp.evaluator import evaluate
from moolisp.env import Environment, get_default_env
from moolisp.types import Macro, boolean, integer, is_macro

class TestMacros:

    def test_defining_macro(self):
        """(macro ...) should return something of type macro"""

        macro = evaluate(["macro", ["foo", "bar"], ["quote", ["bar", "foo"]]], 
            Environment())
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

    def test_expanding_recursive_macro(self):
        """Recursive macros just keep on expanding if recursive call is root

        Based on this clojure example:

            user=> (defmacro test [x] `(test ~x))
            #'user/test
            user=> (macroexpand-1 '(test true))
            (user/test true)
            user=> (macroexpand-1 (macroexpand-1 (macroexpand-1 '(test true))))
            (user/test true)
            user=> (macroexpand '(test true))
            StackOverflowError   clojure.lang.ASeq.more (ASeq.java:116)
        """

        env = Environment()
        interpret("""(define test 
                        (macro (x) 
                            `(test ,x)))""", env)
        assert_equals("(test #t)", 
            interpret("(expand-1 '(test #t))", env))  
        assert_equals("(test #t)", 
            interpret("(expand-1 (expand-1 '(test #t)))", env))  
        assert_equals("(test #t)", 
            interpret("(expand-1 (expand-1 (expand-1 '(test #t))))", env))  

    def test_expand_expands_until_form_is_not_macro_call(self):
        """Expansion continues until root element of result isn't macro call.

        Clojure example:

            user=> (defmacro unless [pred a b] `(if ~pred ~b ~a))
            #'user/unless
            user=> (defmacro test [x] `(unless ~x 'foo 'bar))
            #'user/test
            user=> (macroexpand-1 '(test true))
            (user/unless true (quote user/foo) (quote user/bar))
            user=> (macroexpand '(test true))
            (if true (quote user/bar) (quote user/foo))
        """
        env = Environment()#get_default_env()

        # interpret("""(define expand
        #                 (lambda (exp)
        #                     (if (= exp (expand-1 exp))
        #                         exp
        #                         (expand exp))))""", env)
        #interpret("""(define expand (lambda (x) (expand-1 x)))""", env)

        interpret("""(define unless 
                        (macro (pred a b) 
                            `(if ,pred ,b ,a)))""", env)
        interpret("""(define test 
                        (macro (x) 
                            `(unless ,x 'foo 'bar)))""", env)

        assert_equals("(unless #t 'foo 'bar)", 
            interpret("(expand-1 '(test #t))", env))  
        
        assert_equals("(if #t 'bar 'foo)",
            interpret("(expand '(test #t))", env))  
