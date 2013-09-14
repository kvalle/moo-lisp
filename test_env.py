from nose.tools import assert_equals, assert_raises_regexp
from moolisp import LispNamingError, Environment

class TestEnvironment:

    def test_simple_lookup(self):
        env = Environment({"var": 42})
        assert_equals(42, env["var"])

    def test_lookup_from_inner_env(self):
        outer = Environment({"var": 42})
        inner = Environment({"foo": "bar"}, outer)
        assert_equals(42, inner["var"])

    def test_finding_defining_env(self):
        outer = Environment({"my-var": 1})
        inner = Environment(outer=outer)
        assert_equals(outer, inner.defining_env("my-var"))

    def test_changing_var_in_outer_env(self):
        env = Environment(outer=Environment({"my-var": 1}))
        env.defining_env("my-var")["my-var"] = 2
        assert_equals(2, env["my-var"])

    def test_lookup_deeply_nested_var(self):
        env = Environment(outer=Environment(
            outer=Environment(outer=Environment({"foo": 100}))))
        assert_equals(100, env["foo"])

    def test_lookup_on_missing_raises_exception(self):
        with assert_raises_regexp(LispNamingError, "my-missing-var"):
            Environment()["my-missing-var"]
