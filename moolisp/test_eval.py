from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_false, assert_is_instance

from interpreter import evaluate, parse
from types import Closure, Lambda, Builtin
from errors import LispNamingError, LispSyntaxError, LispTypeError
from env import Environment, get_default_env

class TestEval:

    def test_simple_lookup_from_env(self):
        env = Environment({"foo": 42, "bar": True})
        assert_equals(42, evaluate("foo", env))

    def test_lookup_missing_variable(self):
        with assert_raises_regexp(LispNamingError, "my-var"):
            evaluate("my-var", Environment())

    def test_eval_integer(self):
        assert_equals(42, evaluate(42, Environment()))

    def test_eval_boolean(self):
        assert_equals(True, evaluate(True, Environment()))
        assert_equals(False, evaluate(False, Environment()))

    def test_simple_if_statement(self):
        ast = ["if", True, 42, 1000]
        assert_equals(42, evaluate(ast, Environment()))

    def test_if_with_variable_lookup(self):
        ast = ["if", "pred", "then", "else"]
        env = Environment({"pred": False, "else": 42})
        assert_equals(42, evaluate(ast, env))

    def test_wrong_if_syntax(self):
        with assert_raises_regexp(LispSyntaxError, "Malformed if"):
            evaluate(["if", "with", "far", "too", "many", "parts"], Environment())

    def test_define(self):
        ast = ["define", "x", 1000]
        env = Environment()
        evaluate(ast, env)
        assert_equals(1000, env["x"])

    def test_wrong_define_syntax(self):
        with assert_raises_regexp(LispSyntaxError, "Malformed define"):
            evaluate(["define", "x"], Environment())

    def test_lambda_evaluates_to_lambda_which_is_a_closure(self):
        "The lambda form should evaluate to a lambda object extending closure"
        ast = ["lambda", [], 42]
        lm = evaluate(ast, Environment())
        assert_is_instance(lm, Lambda) 
        assert_is_instance(lm, Closure) 

    def test_lambda_closure_keeps_defining_env(self):
        "The lambda closure needs to keep a copy of the environment where it was defined"
        env = Environment({"foo": 1, "bar": 2})
        ast = ["lambda", [], 42]
        lm = evaluate(ast, env)
        assert_equals(lm.env, env) 

    def test_lambda_closure_holds_function(self):
        "The function part of the lambda closure is the parameters and the body"
        params = ["x", "y"]
        body = ["+", "x", "y"]
        ast = ["lambda", params, body]
        lm = evaluate(ast, Environment)
        assert_equals(lm.params, params)
        assert_equals(lm.body, body)

    def test_call_to_non_function(self):
        "Should raise a TypeError when a non-closure is called as a function"
        with assert_raises(LispTypeError):
            evaluate([True, 1, 2], Environment())
        with assert_raises(LispTypeError):
            evaluate(["foo", 1, 2], Environment({"foo": 42}))

    def test_calling_with_wrong_number_of_arguments(self):
        env = Environment()
        evaluate(["define", "fn", ["lambda", ["x", "y"], 42]], env)
        with assert_raises_regexp(LispTypeError, "expected 2"):
            evaluate(["fn", 1], env)

    def test_calling_simple_function(self):
        assert_equals(42, evaluate([["lambda", [], 42]], Environment()))

    def test_defining_lambda_with_error(self):
        """Tests that the lambda body is not being evaluated when the lambda
        is evaluated or defined. (It should first be evaluated when the function
        is later invoced.)"""
    
        ast = parse("""
            (define fn-with-error
                (lambda (x y)
                    (function body that would never work)))
        """)
        evaluate(ast, Environment())

    def test_lambda_with_free_var(self):
        """Tests that the lambda have access to variables 
        from the environment in which it was defined"""

        env = Environment({"free-variable": 100})
        ast = [["lambda", [], "free-variable"]]
        assert_equals(100, evaluate(ast, env))

    def test_lambda_with_argument(self):
        """Test that the arguments are included in the environment when 
        the function body is evaluated"""

        ast = [["lambda", ["x"], "x"], 42]
        assert_equals(42, evaluate(ast, Environment()))

    def test_lambda_with_argument_and_env(self):
        """Test that arguments overshadow variables defined in the environment
        when the function body is evaluated"""

        env = Environment({"x": 1})
        ast = [["lambda", ["x"], "x"], 2]
        assert_equals(2, evaluate(ast, env))

    def test_defining_then_looking_up_function(self):
        """Test calling named function that's been previously defined 
        from the environment"""

        env = Environment()
        evaluate(["define", "my-fn", ["lambda", ["x"], "x"]], env)
        assert_equals(42, evaluate(["my-fn", 42], env))

    def test_calling_function_recursively(self):
        """Tests that a named function is included in the environment
        where it is evaluated"""
        
        oposite = """
            (define oposite
                (lambda (p) 
                    (if p #f #t)))
        """
        fn = """ 
            (define fn 
                ;; Meaningless (albeit recursive) function
                (lambda (x) 
                    (if x 
                        (fn (oposite x))
                        1000)))
        """
        
        env = Environment()
        evaluate(parse(oposite), env)
        evaluate(parse(fn), env)

        assert_equals(1000, evaluate(["fn", True], env))
        assert_equals(1000, evaluate(["fn", False], env))

    def test_begin_form(self):
        """Testing evaluating expressions in sequence with the begin 
        special form"""

        env = Environment()
        result = evaluate(parse("""
            (begin 
                (define foo 1)
                (define bar 2)
                foo)
        """), env)

        assert_equals(1, result)
        assert_equals(Environment({"foo": 1, "bar": 2}), env)

    def test_empty_begin(self):
        """The begin form should throw a syntax error if there are
        no expressions to be evaluated"""

        with assert_raises_regexp(LispSyntaxError, "begin.*empty"):
            evaluate(["begin"], Environment())

    def test_quote(self):
        """Quoting returns the expression being quoted without evaluating it."""

        ast = ["quote", ["foo", ["+", 1, 2], ["*", 4, 10]]]
        assert_equals(ast[1], evaluate(ast, Environment()))

    def test_set_bang(self):
        """The set! special form updates an already defined variable."""

        env = Environment({"x": 1})
        ast = ["set!", "x", 2]
        evaluate(ast, env)
        assert_equals(2, env["x"])

    def test_set_bang_on_undefined_variable(self):
        """Only defined variables can be updated."""

        with assert_raises_regexp(LispNamingError, "undefined"):
            evaluate(["set!", "wtf", True], Environment())

    def test_set_bang_only_updates_visible_variable(self):
        """Only the innermost (visible) variable binding should be updated"""

        outer = Environment({"x": 1})
        middle = Environment({"x": 2}, outer)
        inner = Environment({}, middle)

        evaluate(["set!", "x", 3], inner)

        assert_false("x" in inner)
        assert_equals(3, middle["x"])
        assert_equals(1, outer["x"])

    def test_calling_a_builtin_function(self):
        "Tests that calling a builtin function gives the expected result"

        env = Environment({'+': Builtin(lambda a, b: a + b)})
        assert_equals(4, evaluate(["+", 2, 2], env))

    def test_calling_builtin_forces_argument_evaluation(self):
        """When biltins (like regular lambdas) are call-by-value, 
        and arguments thould therefore be evaluated before sending them on"""

        env = Environment({'x': 2, '+': Builtin(lambda a, b: a + b)})
        ast = ['+', ['if', True, 2, 'whatever'], 'x']
        assert_equals(4, evaluate(ast, env))

    def test_default_builtin_functions(self):
        """A quick check on some of the default builtins"""

        env = get_default_env()
        assert_equals(5, evaluate(['+', 2, 3], env))
        assert_equals(3, evaluate(['-', 5, 2], env))
        assert_equals(8, evaluate(['*', 4, 2], env))
        assert_equals(8, evaluate(['/', 16, 2], env))
        assert_equals(1, evaluate(['mod', 5, 2], env))
