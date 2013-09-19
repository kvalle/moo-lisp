# -*- coding: utf-8 -*-

"""
Module defining help-function for use in the REPL.

"""

default = """
  Primitives

    Integers: 1, 2, 3, and, you know, so on
    Booleans: #f, #t


  Special forms
    
    form        usage

    if          → (if <predicate> <then-exp> <else-exp>)
    define      → (define <var> <exp>)    
    lambda      → (lambda ([<parameter> ...]) <exp>)
                → (λ ([<parameter> ...]) <exp>)
    begin       → (begin <exp> [<exp> ...])     
    quote       → (quote <exp>)     
                → '<exp>
    eval        → (eval <exp>)

    for more details:
    
        → (help '<form>) 


  Function calls

    → (<function> [<exp> ...])
  
    If <function> is anything other than the special forms defined 
    above, it is evaluated and invoced as a function. The <exp>s 
    are evaluated and passed in as arguments.
    
    Examples: 

      ((lambda (x) (+1 x)) 2)
      (sum 1 2 3)

"""

usage = {
    "if": """
  if 
      
      → (if <predicate> <then-exp> <else-exp>)
      
      Evaluates <predicate>, then evaluates *one* of the 
      two other expressions depending the value of <predicate>. 
      <predicate> should evaluate to a boolean (se above).
""", "define": """
  define 

      → (define <var> <exp>)

      evaluates <exp> and then extends the *current* environment 
      with <var> → <evaluated exp>.
""", "lambda": """  
  lambda

      → (lambda ([<parameter> ...]) <exp>)
      → (λ ([<parameter> ...]) <exp>)
      
      Evaluates to a function closure created from the function 
      with the (zero or more) named <parameter>s, and <exp> as 
      the body.
""", "begin": """
  begin

      → (begin <exp> [<exp> ...])  

      Evaluates the expressions in order. Returns the value of 
      the final expression evaluated.
""", "quote": """
  quoting

      → (quote <exp>)
      → '<exp>

      Returns <exp> without evaluating it.
""", "eval": """
  eval

      → (eval <exp>)

      The eval form evaluates whatever is passed to it as a moo-lisp 
      program. This means that <exp> is first evaluated to get its value
      which is then evaluated.

      The eval and quote forms may be seen as opposites, in that
      (eval (quote <exp>)) == <exp>
"""    
}

unknown = """
    Unknown form: '%s'.
    Did you mean one of %s?
"""

def help(form=None):
    if form:
        available = ", ".join("'%s'" % form for form in usage.keys())
        print usage.get(form, unknown % (form, available))
    else:
        print default

if __name__ == '__main__':
    from sys import argv
    help(argv[1]) if len(argv) > 1 else help()
