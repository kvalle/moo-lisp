
                              ^__^         
                MOO           (oo)\_______      
          the not all that    (__)\       )\/\        
            serious lisp          ||----w |           
                                  ||     ||          

Primitives

  Integers: 1, 2, 3, and, you know, so on
  Booleans: #f, #t

Special forms

  if 
      
      → (if <predicate> <then-exp> <else-exp>)
      
      Evaluates <predicate>, then evaluates *one* of the 
      two other expressions depending the value of <predicate>. 
      <predicate> should evaluate to a boolean (se above).
  
  define 

      → (define var exp)

      evaluates `exp` and then extends the *current* environment 
      with `var` → the evaluated `exp`.
  
  lambda 

      → (lambda ([<parameter> ...]) <expression>)
      
      Evaluates to a function closure created from the function 
      with the (zero or more) named parameters, and <expression> 
      as the body.
  
  sequencing 

      → (begin <exp> [<exp> ...])  

      Evaluates the expressions in order. Returns the value of 
      the final expression evaluated.
  
  function call 

      → (<function> [<exp> ...])

      If <function> is anything other than the special forms defined 
      above, it is evaluated and invoced as a function. The `exp`s 
      are evaluated and passed in as arguments.
      
      Examples: 
        ((lambda (x) (+1 x)) 2)
        (sum 1 2 3)
