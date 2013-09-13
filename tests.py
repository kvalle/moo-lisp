from unittest.case import SkipTest
from nose.tools import eq_

import mylisp
from mylisp import tokenize

class TestMyLisp:

    def setup(self):
        self.lisp = mylisp.Lisp()

    def test_factorial_program(self):
        raise SkipTest("We're not quite there yet")
        program = """
            (define fact
                (lambda (n)
                    (if (<= n 1)
                        1 
                        (* n (fact (- n 1))))))
        """
        self.lisp.interpret(program)
        eq_(120, self.lisp.interpret("(fact 5)"))

    def test_tokenize_single_atom(self):
        eq_(["foo"], tokenize("foo"))

    def test_tokenize_list(self):
        source = "(foo 1 2)"
        tokens = ["(", "foo", "1", "2", ")"]
        eq_(tokens, tokenize(source))
