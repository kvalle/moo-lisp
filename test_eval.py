from nose.tools import assert_equals, assert_raises_regexp

import mylisp
from mylisp import evaluate
from mylisp import LispNamingError

class TestEval:

    def test_simple_lookup_from_env(self):
        env = {"foo": 42, "bar": True}
        assert_equals(42, evaluate("foo", env))

    def test_lookup_missing_variable(self):
        with assert_raises_regexp(LispNamingError, "my-var"):
            evaluate("my-var", {})
