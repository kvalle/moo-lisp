
def tokenize(s):
    return s.replace("(", " ( ").replace(")", " ) ").split()

class Lisp:

    def interpret(self, s):
        raise NotImplementedError

