# -*- coding: utf-8 -*-

import unittest
from nose.tools import assert_equals, assert_raises, assert_raises_regexp

from moolisp.parser import parse, unparse, expand_quote_ticks, \
    find_matching_paren, expand_quoted_symbol, expand_quoted_list
from moolisp.errors import LispSyntaxError

class TestParsingQuotes:

    ## Tests for find_matching_paren function

    def test_find_matching_paren(self):
        source = "(foo (bar) '(this ((is)) quoted))"
        assert_equals(32, find_matching_paren(source, 0))
        assert_equals(9, find_matching_paren(source, 5))

    def test_find_matching_empty_parens(self):
        assert_equals(1, find_matching_paren("()", 0))

    def test_find_matching_paren_throws_exception_on_bad_initial_position(self):
        """If asked to find closing paren from an index where there is no opening
        paren, the function should raise an error"""

        with assert_raises(AssertionError):
            find_matching_paren("string without parens", 4)

    def test_find_matching_paren_throws_exception_on_no_closing_paren(self):
        """The function should raise error when there is no matching paren to be found"""

        with assert_raises_regexp(LispSyntaxError, "Unbalanced expression"):
            find_matching_paren("string (without closing paren", 7)

    ## Tests for expanding quoted symbols

    def test_expand_single_quoted_symbol(self):
        assert_equals("(foo (quote bar))", expand_quoted_symbol("(foo 'bar)"))
        assert_equals("(foo (quote #t))", expand_quoted_symbol("(foo '#t)"))
        assert_equals("(foo (quote +))", expand_quoted_symbol("(foo '+)"))

    def test_expand_quoted_symbol_dont_touch_nested_quote_on_list(self):
        source = "(foo ''(bar))"
        assert_equals(source, expand_quoted_symbol(source))

    def test_expand_quotes_with_only_symbols(self):
        assert_equals("(quote foo)", expand_quote_ticks("'foo"))
        assert_equals("(quote (quote (quote foo)))", expand_quote_ticks("'''foo"))

    def test_parse_quote_tick_on_symbol(self):
        assert_equals(["quote", "foo"], parse("'foo"))
        assert_equals(["quote", "+"], parse("'+"))

    def test_parse_quote_tick_on_atom(self):
        assert_equals(["quote", 1], parse("'1"))
        assert_equals(["quote", True], parse("'#t"))

    def test_nested_quotes(self):
        assert_equals(["quote", ["quote", "foo"]], parse("''foo"))
        assert_equals(["quote", ["quote", ["quote", "foo"]]], parse("'''foo"))

    ## Tests for expanding quoted lists

    def test_expand_single_quoted_list(self):
        assert_equals("(foo (quote (+ 1 2)))", expand_quoted_list("(foo '(+ 1 2))"))
        assert_equals("(foo (quote (#t #f)))", expand_quoted_list("(foo '(#t #f))"))

    def test_expand_quotes_with_lists(self):
        assert_equals("(quote (foo bar))", expand_quote_ticks("'(foo bar)"))
        assert_equals("(quote (quote (quote (foo bar))))", 
            expand_quote_ticks("'''(foo bar)"))

    def test_parse_quote_tick_on_list(self):
        assert_equals(["quote", ["foo", "bar"]], parse("'(foo bar)"))
        assert_equals(["quote", []], parse("'()"))

    def test_nested_quotes_on_lists(self):
        assert_equals(["quote", ["quote", ["foo", "bar"]]], parse("''(foo bar)"))

