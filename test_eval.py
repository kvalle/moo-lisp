from nose.tools import assert_equals, assert_raises_regexp

from mylisp import evaluate
from mylisp import LispNamingError

class TestEval:

    def test_simple_lookup_from_env(self):
        env = {"foo": 42, "bar": True}
        assert_equals(42, evaluate("foo", env))

    def test_lookup_missing_variable(self):
        with assert_raises_regexp(LispNamingError, "my-var"):
            evaluate("my-var", {})

    def test_eval_integer(self):
        assert_equals(42, evaluate(42))

    def test_eval_boolean(self):
        assert_equals(True, evaluate(True))
        assert_equals(False, evaluate(False))

    def test_simple_if_statement(self):
        ast = ["if", True, 42, 1000]
        assert_equals(42, evaluate(ast))

    def test_if_with_variable_lookup(self):
        ast = ["if", "pred", "then", "else"]
        env = {"pred": False, "else": 42}
        assert_equals(42, evaluate(ast, env))
