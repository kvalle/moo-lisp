from nose.tools import assert_equals, assert_raises_regexp

from interpreter import evaluate, parse
from errors import LispNamingError, LispSyntaxError
from env import Environment

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

    def test_lambda_with_no_free_vars(self):
        "Tests that the lambda executes it's body when called"
        
        ast = ["lambda", [], 42]
        fn = evaluate(ast, Environment())
        assert_equals(42, fn())

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

        ast = ["lambda", [], "free-variable"]
        fn = evaluate(ast, Environment({"free-variable": 100}))
        assert_equals(100, fn())

    def test_lambda_with_argument(self):
        """Test that the arguments are included in the environment when 
        the function body is evaluated"""

        ast = ["lambda", ["x"], "x"]
        fn = evaluate(ast, Environment())
        assert_equals("foo", fn("foo"))

    def test_defining_then_looking_up_function(self):
        """Sanity check that we can hold and look up functions in the
        environment"""

        env = Environment()
        evaluate(["define", "my-fn", ["lambda", ["x"], "x"]], env)
        assert_equals("foo", env["my-fn"]("foo"))

    def test_calling_simple_function(self):
        """Test calling named function that's been previously defined 
        from the environment"""

        env = Environment()
        evaluate(["define", "my-fn", ["lambda", ["x"], "x"]], env)
        assert_equals(42, evaluate(["my-fn", 42], env))

    def test_calling_lambda_directly(self):
        """Tests that it's is possible to define a lambda function and
        then calling it directly"""

        assert_equals(42, evaluate([["lambda", ["x"], "x"], 42], Environment()))

    def test_calling_function_recursively(self):
        """Tests that a named function is included in the environment
        where it is evaluated"""

        # Starting env out with some "standard functions" this time
        import operator
        env = Environment({
            '-': operator.sub, 
            '>': operator.gt
        })
        
        # Meaningless (albeit recursive) function
        program = """
            (define fn 
                (lambda (x) 
                    (if (> x 0) 
                        (fn (- x 1))
                        1000)))
        """
        evaluate(parse(program), env)
        assert_equals(1000, evaluate(["fn", 10], env))

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
