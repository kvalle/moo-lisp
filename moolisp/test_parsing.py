# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp

from interpreter import tokenize, parse
from errors import LispSyntaxError

class TestParsing:

    def test_tokenize_single_atom(self):
        assert_equals(['foo'], tokenize('foo'))

    def test_tokenize_list(self):
        source = '(foo 1 2)'
        tokens = ['(', 'foo', '1', '2', ')']
        assert_equals(tokens, tokenize(source))

    def test_parse_on_simple_list(self):
        program = '(foo bar)'
        assert_equals(['foo', 'bar'], parse(program))

    def test_parse_on_tested_list(self):
        program = '(foo (bar x y) (baz x))'
        ast = ['foo', 
                ['bar', 'x', 'y'], 
                ['baz', 'x']]
        assert_equals(ast, parse(program))

    def test_parse_exception_missing_paren(self):
        with assert_raises_regexp(LispSyntaxError, 'Unexpected EOF'):
            parse('(foo (bar x y)')

    def test_parse_exception_extra_paren(self):
        with assert_raises_regexp(LispSyntaxError, 'Expected EOF'):
            parse('(foo (bar x y)))')

    def test_parse_with_types(self):
        program = '(if #f (* 42 x) 100)'
        ast = ['if', False, ['*', 42, 'x'], 100]
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
        expected_ast = ['define', 'variable', ['if', True, 42, ['something', 'else']]]
        assert_equals(expected_ast, parse(program))

    def test_parse_quote_tick_on_symbol(self):
        assert_equals(["quote", "foo"], parse("'foo"))
        assert_equals(["quote", "+"], parse("'+"))

    def test_parse_quote_tick_on_list(self):
        assert_equals(["quote", ["foo", "bar"]], parse("'(foo bar)"))
        assert_equals(["quote", []], parse("'()"))
