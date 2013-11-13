# -*- coding: utf-8 -*-

from nose.tools import assert_equals

from moolisp.interpreter import interpret, default_env

class TestMooLisp:
    """Testing the implementation with a few non-trivial programs"""

    def test_factorial(self):
        """Simple factorial"""
        env = default_env()
        interpret("""
            (define fact
                (lambda (n)
                    (if (<= n 1)
                        1 
                        (* n (fact (- n 1))))))
        """, env)
        assert_equals("120", interpret("(fact 5)", env))

    def test_gcd(self):
        """Greates common dividor"""
        env = default_env()
        interpret("""
            (define gcd
                (lambda (a b)
                    (if (= 0 b)
                        a 
                        (gcd b (mod a b)))))
        """, env)
        assert_equals("6", interpret("(gcd 108 30)", env))
        assert_equals("1", interpret("(gcd 17 5)", env))
