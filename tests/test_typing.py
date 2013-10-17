# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_true, assert_false

from moolisp.types import tag, is_type, type_of, value_of, true, false

class TestTyping:

    def test_creating_type_is_type(self):
        t = tag('footype', 42)
        assert_true(is_type(t))

    def test_getting_value_of_type(self):
        t = tag('footype', 42)
        assert_equals(42, value_of(t))

    def test_getting_type_of_type(self):
        t = tag('footype', 42)
        assert_equals('footype', type_of(t))

    def test_true(self):
        assert_true(value_of(true))

    def test_false(self):
        assert_false(value_of(false))
