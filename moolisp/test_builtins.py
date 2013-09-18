from nose.tools import assert_equals, assert_true, assert_false

from interpreter import interpret
from env import get_default_env

class TestBuiltins:

    def test_arithmetic_functions(self):
        """Sanity check for the builtin artihmetic functions"""

        env = get_default_env()
        assert_equals(5, interpret('(+ 2 3)', env))
        assert_equals(3, interpret('(- 5 2)', env))
        assert_equals(8, interpret('(* 4 2)', env))
        assert_equals(8, interpret('(/ 16 2)', env))
        assert_equals(1, interpret('(mod 5 2)', env))

    def test_comparator_functions(self):
        """Sanity check for the builtin comparators"""

        env = get_default_env()
        assert_true(interpret('(= 2 2)', env))
        assert_false(interpret('(= 2 3)', env))
        assert_true(interpret('(= #t #t)', env))
        assert_false(interpret('(> 1 2)', env))
        assert_true(interpret('(> 2 1)', env))
        assert_true(interpret('(< 1 2)', env))
        assert_false(interpret('(< 2 1)', env))
        assert_true(interpret('(>= 2 1)', env))
        assert_true(interpret('(>= 2 2)', env))
        assert_false(interpret('(>= 2 3)', env))
        assert_false(interpret('(<= 2 1)', env))
        assert_true(interpret('(<= 2 2)', env))
        assert_true(interpret('(<= 2 3)', env))

    def test_list_nil(self):
        """Test the predefined nil value"""

        env = get_default_env()
        assert_equals(interpret("(quote ())", env), interpret("nil", env))
        assert_equals([], interpret("nil", env))

    def test_creating_lists(self):
        """Test different ways to create lists"""

        env = get_default_env()
        xs = [1, 2, "foo", 4]
        assert_equals(xs, interpret("(quote (1 2 foo 4))", env))
        assert_equals(xs, interpret("(cons 1 (cons 2 (cons 'foo (cons 4 nil))))", env))
        assert_equals(xs, interpret("(list 1 2 'foo 4)", env))

    def test_deconstruction_of_lists(self):
        """Tests picking elements from lists using car and cdr"""

        env = get_default_env()
        interpret("(define lst (list 1 2 3 4 5))", env)
        assert_equals(1, interpret("(car lst)", env))
        assert_equals(2, interpret("(car (cdr lst))", env))
        assert_equals([3, 4, 5], interpret("(cdr (cdr lst))", env))
