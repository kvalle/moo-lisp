# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises, assert_raises_regexp

from moolisp.types import boolean, integer
from moolisp.parser import parse, unparse, find_matching_paren
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

    ## Tests for expanding quoted symbols correctly

    def test_expand_single_quoted_symbol(self):
        assert_equals(["foo", ["quote", "bar"]], parse("(foo 'bar)"))
        assert_equals(["foo", ["quote", boolean(True)]], parse("(foo '#t)"))
        assert_equals(["foo", ["quote", '+']], parse("(foo '+)"))

    def test_expand_quoted_symbol_dont_touch_nested_quote_on_list(self):
        source = "(foo ''(bar))"
        assert_equals(source, unparse(parse(source)))

    def test_expand_quotes_with_only_symbols(self): 
        assert_equals(["quote", "foo"], parse("'foo"))
        assert_equals(["quote", ["quote", ["quote", "foo"]]], parse("'''foo"))

    def test_parse_quote_tick_on_symbol(self):
        assert_equals(["quote", "foo"], parse("'foo"))
        assert_equals(["quote", "+"], parse("'+"))

    def test_parse_quote_tick_on_atom(self):
        assert_equals(["quote", integer(1)], parse("'1"))
        assert_equals(["quote", boolean(True)], parse("'#t"))

    def test_nested_quotes(self):
        assert_equals(["quote", ["quote", "foo"]], parse("''foo"))
        assert_equals(["quote", ["quote", ["quote", "foo"]]], parse("'''foo"))

    ## Tests for expanding quoted lists

    def test_expand_single_quoted_list(self):
        assert_equals(["foo", ["quote", ["+", integer(1), integer(2)]]], 
            parse("(foo '(+ 1 2))"))
        assert_equals(["foo", ["quote", [boolean(True), boolean(False)]]], parse("(foo '(#t #f))"))

    def test_expand_quotes_with_lists(self):
        assert_equals(["quote", ["foo", "bar"]], parse("'(foo bar)"))
        assert_equals(["quote", ["quote", ["quote", ["foo", "bar"]]]],
            parse("'''(foo bar)"))

    def test_parse_quote_tick_on_list(self):
        assert_equals(["quote", ["foo", "bar"]], parse("'(foo bar)"))
        assert_equals(["quote", []], parse("'()"))

    def test_nested_quotes_on_lists(self):
        assert_equals(["quote", ["quote", ["foo", "bar"]]], parse("''(foo bar)"))

    ## Tests for expanding quasiquote and unquote
    
    def test_expand_quasiquoted_symbol(self):
        assert_equals(["quasiquote", "foo"], parse("`foo"))
        assert_equals(["quasiquote", "+"], parse("`+"))
        assert_equals(["quasiquote", boolean(False)], parse("`#f"))

    def test_expand_quasiquoted_list(self):
        assert_equals(["quasiquote", ["+", integer(1), integer(2)]], parse("`(+ 1 2)"))

    def test_nested_quasiquotes(self):
        assert_equals(["quasiquote", ["quasiquote", ["quasiquote", "foo"]]],
            parse("```foo"))
        assert_equals(["quasiquote", 
                        ["quasiquote", 
                          ["quasiquote", ["+", integer(1), integer(2)]]]],
            parse("```(+ 1 2)"))

    def test_expand_unquoted_symbol(self):
        assert_equals(["unquote", "foo"], parse(",foo"))
        assert_equals(["unquote", "+"], parse(",+"))
        assert_equals(["unquote", boolean(False)], parse(",#f"))

    def test_expand_unquoted_list(self):
        assert_equals(["unquote", ["+", integer(1), integer(2)]], parse(",(+ 1 2)"))

    def test_quasiqute_with_unquote(self):
        assert_equals(["quasiquote", 
                        ["+", ["unquote", "foo"], ["unquote", "bar"], integer(42)]],
            parse("`(+ ,foo ,bar 42)"))

    def test_expand_quote_combinations(self):
        assert_equals(["quasiquote", ["quote", ["unquote", "foo"]]],
            parse("`',foo"))

    def test_expand_crazy_quote_combo(self):
        source = "`(this ,,'`(makes ,no) 'sense)"
        assert_equals(source, unparse(parse(source)))
