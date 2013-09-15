;; Some example code, whoo!

;; To run the code:
;;
;;    ./moo example.moo
;;

(define fact 
    ;; Factorial function
    (lambda (n) 
        (if (<= n 1) 
            1 ; Look ma, inline comment!
            (* n (fact (- n 1))))))

;; When parsing the file, the last statement is returned
(fact 5)
