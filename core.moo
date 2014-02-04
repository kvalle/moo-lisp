(define nil '())

(define nil? (lambda (x)
    (eq x 'nil)))

(define if (macro (pred then else)
    `(cond (,pred ,then)
           (#t ,else))))
