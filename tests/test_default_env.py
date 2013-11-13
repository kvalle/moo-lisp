# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from moolisp.interpreter import interpret

class TestDefaultEnvironment:

    def test_list_nil(self):
        """Test the predefined nil value"""

        assert_equals(interpret("(quote ())"), interpret("nil"))
        assert_equals("()", interpret("nil"))
