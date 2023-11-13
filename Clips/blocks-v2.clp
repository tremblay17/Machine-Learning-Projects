(deffacts initial-state
    ; Define your initial block configuration here
    (on A B)
    (on B C)
    (on C table)
    (on-table C)

    (on D E)
    (on E F)
    (on F table)
    (on-table F)
)

(deffacts goal-state
    ; Define your desired goal state here
    (on D C)
    (on C B)
    (on A table)
    (on F E)
    (on E table)
)

(defrule pick-up
    ?h <- (hand empty)
    ?b <- (on ?block ?support)
    =>
    (retract ?h)
    (retract ?b)
    (assert (block ?block in-hand))
)

(defrule put-down
    ?h <- (hand in-hand)
    ?b <- (block ?block in-hand)
    =>
    (retract ?h)
    (retract ?b)
    (assert (on ?block table))
)

(defrule stack
    ?h <- (hand empty)
    ?b1 <- (on ?block1 ?support1)
    ?b2 <- (on ?block2 ?support2)
    (test (neq ?block1 ?block2))
    =>
    (retract ?h)
    (retract ?b1)
    (retract ?b2)
    (assert (on ?block1 ?block2))
)

(defrule unstack
    ?h <- (hand empty)
    ?b1 <- (on ?block1 ?block2)
    =>
    (retract ?h)
    (retract ?b1)
    (assert (on ?block1 table))
)

(defrule move
    ?h <- (hand empty)
    ?b1 <- (on ?block1 ?from)
    ?b2 <- (on ?block2 ?to)
    (test (neq ?block1 ?block2))
    =>
    (retract ?h)
    (retract ?b1)
    (retract ?b2)
    (assert (on ?block1 ?to))
)

(defrule finish
    (hand empty)
    =>
    (printout t "Finished!" crlf)
)

(defrule start
    (declare (salience -10))
    =>
    (assert (hand empty))
)

