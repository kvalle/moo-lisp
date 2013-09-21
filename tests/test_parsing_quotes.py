# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from moolisp.parser import parse, unparse, expand_quote_ticks
import unittest

@unittest.skip("showing class skipping")
class TestParsingQuotes:

    def test_parse_quote_tick_on_symbol(self):
        assert_equals(["quote", "foo"], parse("'foo"))
        assert_equals(["quote", "+"], parse("'+"))

    def test_parse_quote_tick_on_atom(self):
        assert_equals(["quote", 1], parse("'1"))
        assert_equals(["quote", True], parse("'#t"))

    def test_nested_quotes(self):
        assert_equals(["quote", ["quote", "foo"]], parse("''foo"))
        assert_equals(["quote", ["quote", ["quote", "foo"]]], parse("'''foo"))
        assert_equals(["quote", ["quote", ["foo", "bar"]]], parse("''(foo bar)"))

    def test_parse_quote_tick_on_list(self):
        assert_equals(["quote", ["foo", "bar"]], parse("'(foo bar)"))
        assert_equals(["quote", []], parse("'()"))

    def test_expand_quote_tick(self):
        assert_equals("(quote foo)", expand_quote_ticks("'foo"))
        assert_equals("(quote (quote (quote foo)))", expand_quote_ticks("'''foo"))

        assert_equals("(quote (foo bar))", expand_quote_ticks("'(foo bar)"))
        assert_equals("(quote (quote (quote (foo bar))))", 
            expand_quote_ticks("'''(foo bar)"))
    
    def test_expand_quasiquote(self):
        assert_equals("(quasiquote foo)", expand_quote_ticks("`foo"))
        assert_equals("(quasiquote (+ 1 2))", expand_quote_ticks("`(+ 1 2)"))
        assert_equals("(quasiquote (quasiquote (quasiquote (+ 1 2))))",
            expand_quote_ticks("```(+ 1 2)"))

    def test_expand_quote_combinations(self):
        assert_equals("(quasiquote (quote (unquote foo)))", expand_quote_ticks("`',foo"))

    def test_expand_crazy_quote_combo(self):
        source = "`(this ,,'`(makes ,no) 'sense)"
        assert_equals(source, unparse(parse(source)))
