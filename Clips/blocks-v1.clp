(deffacts init-state
    (stack A B C)
    (stack D E F)
)

(defrule initial-state
  (not (block ?))
  =>
  (assert (block A on-table))
  (assert (block B on-table))
  (assert (block C on-table))
  (assert (block D on-table))
  (assert (block E on-table))
  (assert (block F on-table))
)

(defrule goal-state
  (block A)
  (block B)
  (block C)
  (block D)
  (block E)
  (block F)
  =>
  (printout t "Goal state achieved!" crlf)
)

(defrule pick-up
  ?b <- (block ?block on-table)
  ?h <- (hand empty)
  =>
  (retract ?b ?h)
  (assert (block ?block in-hand))
)

(defrule put-down
  ?b <- (block ?block in-hand)
  ?h <- (hand empty)
  =>
  (retract ?b ?h)
  (assert (block ?block on-table))
)

(defrule stack
  ?b1 <- (block ?block1 in-hand)
  ?b2 <- (block ?block2 on ?on)
  ?h <- (hand empty)
  (test (neq ?block1 ?block2))
  =>
  (retract ?b1 ?b2 ?h)
  (assert (block ?block1 on ?block2))
)

(defrule unstack
  ?b1 <- (block ?block1 on ?block2)
  ?b2 <- (block ?block2 in-hand)
  ?h <- (hand empty)
  =>
  (retract ?b1 ?b2 ?h)
  (assert (block ?block1 on-table))
)

(defrule move
  ?b1 <- (block ?block1 on ?from)
  ?b2 <- (block ?block2 on ?to)
  ?h <- (hand empty)
  (test (neq ?block1 ?block2))
  =>
  (retract ?b1 ?b2 ?h)
  (assert (block ?block1 on ?to))
)

(defrule legal-move
  ?b1 <- (block ?block1 on ?from)
  ?h <- (hand empty)
  (or (block ?block2 in-hand)
      (not (block ?block2)))
  =>
  (retract ?b1 ?h)
  (assert (block ?block1 on-table))
)

(defrule goal-state-check
  ?b <- (block ?block on ?to)
  =>
  (retract ?b)
  (assert (block ?block))
)

(defrule start
  (declare (salience -10))
  =>
  (assert (hand empty))
)

(defrule finish
  ?h <- (hand empty)
  =>
  (retract ?h)
  (printout t "Finished!" crlf)
)
