# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises_regexp, \
    assert_raises, assert_false, assert_is_instance

from moolisp.evaluator import evaluate
from moolisp.parser import parse
from moolisp.types import Closure, Lambda, Builtin
from moolisp.errors import LispNamingError, LispSyntaxError, LispTypeError
from moolisp.env import Environment

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
        """Test evaluation of expressions (variable lookup) within if form"""

        ast = ["if", "pred", "then", "else"]
        env = Environment({"pred": False, "else": 42})
        assert_equals(42, evaluate(ast, env))

    def test_atom(self):
        env = Environment()
        assert_equals(True, evaluate(["atom", True], env))
        assert_equals(True, evaluate(["atom", False], env))
        assert_equals(True, evaluate(["atom", 42], env))
        assert_equals(True, evaluate(["atom", "foo"], Environment({"foo": "bar"})))
        assert_equals(False, evaluate(["atom", "foo"], Environment({"foo": ["bar"]})))
        assert_equals(False, evaluate(["atom", ["quote", ["foo", "bar"]]], env))

    def test_wrong_if_syntax(self):
        """Test evaluating if expression with too many parts"""

        with assert_raises_regexp(LispSyntaxError, "Malformed if"):
            evaluate(["if", "with", "far", "too", "many", "parts"], Environment())

    def test_define(self):
        """Test simplest possible define"""

        env = Environment()
        evaluate(["define", "x", 1000], env)
        assert_equals(1000, env["x"])

    def test_define_with_wrong_number_of_arguments(self):
        """Defines should have exactly two arguments, or raise an error"""

        with assert_raises_regexp(LispSyntaxError, "Wrong number of arguments"):
            evaluate(["define", "x"], Environment())

        with assert_raises_regexp(LispSyntaxError, "Wrong number of arguments"):
            evaluate(["define", "x", 1, 2], Environment())

    def test_define_with_nonsymbol_as_variable(self):
        """Malformed defines should throw an error"""

        with assert_raises_regexp(LispSyntaxError, "non-symbol"):
            evaluate(["define", True, 42], Environment())

    def test_lambda_evaluates_to_lambda_which_is_a_closure(self):
        """The lambda form should evaluate to a lambda object extending closure"""

        ast = ["lambda", [], 42]
        lm = evaluate(ast, Environment())
        assert_is_instance(lm, Lambda) 
        assert_is_instance(lm, Closure) 

    def test_lambda_closure_keeps_defining_env(self):
        """The closure should keep a copy of the environment where it was defined"""

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

    def test_using_lambda_character(self):
        """The λ character should be an valid alternaltive to writing "lambda" """

        env = Environment({"x": 42})
        assert_equals(42, evaluate([["λ", [], "x"]], env))
        assert_equals(42, evaluate([["lambda", [], "x"]], env))

    def test_call_to_non_function(self):
        "Should raise a TypeError when a non-closure is called as a function"
        with assert_raises(LispTypeError):
            evaluate([True, 1, 2], Environment())
        with assert_raises(LispTypeError):
            evaluate(["foo", 1, 2], Environment({"foo": 42}))

    def test_calling_with_wrong_number_of_arguments(self):
        """Lambda should raise exception when called with wrong number of arguments"""

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
        """Tests that calling a builtin function gives the expected result"""

        env = Environment({'+': Builtin(lambda a, b: a + b)})
        assert_equals(4, evaluate(["+", 2, 2], env))

    def test_calling_builtin_forces_argument_evaluation(self):
        """Bultins (like the regular lambdas) are call-by-value 
        and the arguments thould therefore be evaluated first"""

        env = Environment({'x': 2, '+': Builtin(lambda a, b: a + b)})
        ast = ['+', ['if', True, 2, 'whatever'], 'x']
        assert_equals(4, evaluate(ast, env))

    def test_eval_simple_expression(self):
        """Eval takes one argument, evaluates it (like all functions) and 
        evaluates the evaluated argument"""

        # equivalent to evaluate("foo")
        with assert_raises_regexp(LispNamingError, "Variable 'foo' is undefined"):
            assert_equals("foo", evaluate(["eval", ["quote", "foo"]], Environment()))

        # equivalent to evaluate(["quote, "foo"])
        ast = ["eval", ["quote", ["quote", "foo"]]]
        assert_equals("foo", evaluate(ast, Environment()))

        # equivalent to evaluate(["quote, ["quote, "foo"]])
        ast = ["eval", ["quote", ["quote", ["quote", "foo"]]]]
        assert_equals(["quote", "foo"], evaluate(ast, Environment()))

    def test_eval_quasiquote_without_unquote(self):
        assert_equals("foo", evaluate(["quasiquote", "foo"], Environment()))
        assert_equals(["+", 1, 2], evaluate(["quasiquote", ["+", 1, 2]], Environment()))

    def test_eval_quasiquote_with_top_level_unquote(self):
        env = Environment({"foo": 42, "bar": 100})
        ast = ["quasiquote", ["+", ["unquote", "foo"], ["unquote", "bar"]]]
        assert_equals(["+", 42, 100], evaluate(ast, env))

    def test_eval_quasiquote_with_deeper_unquotes(self):
        env = Environment({"foo": 42, "bar": 100})
        ast = ["quasiquote", ["+", ["unquote", "foo"], ["+", 1, ["unquote", "bar"]]]]
        assert_equals(["+", 42, ["+", 1, 100]], evaluate(ast, env))

    def test_eval_unquote_outside_of_quasiquote_raises_exception(self):
        """Unquote cannot stand alone, without an *directly enclosing* quasiquote."""

        env = Environment()
        msg = "Unquote outside of quasiquote: ,foo"

        with assert_raises_regexp(LispSyntaxError, msg):
            # standalone unquote
            evaluate(["unquote", "foo"], env)

        with assert_raises_regexp(LispSyntaxError, msg):
            # unquote within another unquote
            ast = ["quasiquote", ["unquote", ["unquote", "foo"]]]
            evaluate(ast, env)

    def test_simple_let_expression(self):
        """Let expressions should create a new environment with the new definitions,
        then evaluate the body with this environment, and not make any changes to 
        the outer environment"""

        env = Environment({"foo": 1})
        ast = parse("(let ((foo 2)) foo)")
        assert_equals(2, evaluate(ast, env))
        assert_equals(1, env["foo"])

    def test_let_raises_error_on_nonsymbol_as_variable(self):
        """Attempting to define something other than a symbol as a variable should
        result in an exception"""

        with assert_raises_regexp(LispSyntaxError, "non-symbol"):
            evaluate(parse("(let ((#t 1)) 1)"), Environment())

    def test_let_raises_error_wrong_number_of_elements(self):
        """A variable definition should consist of only two elements,
        the variable and the value"""

        with assert_raises_regexp(LispSyntaxError, "Wrong number of arguments"):
            evaluate(parse("(let ((foo 1 2)) foo)"), Environment())
