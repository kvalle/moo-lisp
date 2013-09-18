from nose.tools import assert_equals
from interpreter import interpret
from env import get_default_env

class TestMyLisp:

    def test_factorial_program(self):
        env = get_default_env()
        interpret("""
            (define fact
                (lambda (n)
                    (if (<= n 1)
                        1 
                        (* n (fact (- n 1))))))
        """, env)
        assert_equals(120, interpret("(fact 5)", env))
