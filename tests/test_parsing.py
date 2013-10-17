# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp

from moolisp.types import true, false, integer
from moolisp.parser import parse
from moolisp.errors import LispSyntaxError

class TestParsing:

    def test_parse_single_atom(self):
        assert_equals('foo', parse('foo'))

    def test_parse_list_of_symbols(self):
        assert_equals(['foo', 'bar', 'baz'], parse('(foo bar baz)'))

    def test_parse_on_simple_list(self):
        program = '(foo bar)'
        assert_equals(['foo', 'bar'], parse(program))

    def test_parse_on_nested_list(self):
        program = '(foo (bar x y) (baz x))'
        ast = ['foo', 
                ['bar', 'x', 'y'], 
                ['baz', 'x']]
        assert_equals(ast, parse(program))

    def test_parse_exception_missing_paren(self):
        with assert_raises_regexp(LispSyntaxError, 'Unbalanced expression'):
            parse('(foo (bar x y)')

    def test_parse_exception_extra_paren(self):
        with assert_raises_regexp(LispSyntaxError, 'Expected EOF'):
            parse('(foo (bar x y)))')

    def test_parse_with_types(self):
        program = '(if #f (* 42 x) 100)'
        ast = ['if', false, ['*', integer(42), 'x'], integer(100)]
        assert_equals(ast, parse(program))

    def test_parse_comments(self):
        program = """
        ;; this first line is a comment
        (define variable
            ; here is another comment
            (if #t 
                42 ; inline comment!
                (something else)))
        """
        expected_ast = ['define', 'variable', ['if', true, integer(42), ['something', 'else']]]
        assert_equals(expected_ast, parse(program))
