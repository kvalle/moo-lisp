(define nil '())

(define if (macro (pred then else)
    `(cond (,pred ,then)
           (#t ,else))))
