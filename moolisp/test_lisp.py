from nose.tools import assert_equals
from interpreter import interpret
from env import Environment

class TestMyLisp:

    def test_factorial_program(self):
        env = Environment()
        interpret("""
            (define fact
                (lambda (n)
                    (if (<= n 1)
                        1 
                        (* n (fact (- n 1))))))
        """, env)
        assert_equals(120, interpret("(fact 5)", env))
