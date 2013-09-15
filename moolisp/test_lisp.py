from nose.tools import assert_equals
from interpreter import interpret

class TestMyLisp:

    def test_factorial_program(self):
        interpret("""
            (define fact
                (lambda (n)
                    (if (<= n 1)
                        1 
                        (* n (fact (- n 1))))))
        """)
        assert_equals(120, interpret("(fact 5)"))
