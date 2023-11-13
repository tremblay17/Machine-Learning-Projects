(deftemplate stack
   (multislot blocks)
)

(deffacts initial-state
   (stack (blocks A B C))
   (stack (blocks D E F))
)

(deffacts goal-state
   (stack (blocks D C B))
   (stack (blocks A))
   (stack (blocks F E))
)

(deffacts goal-achieved-fact
   (goal-achieved FALSE)
)

(deffunction goal-matched (?goal-stack)
   (bind ?matched TRUE)
   (loop-for-count (?i (length$ ?goal-stack))
      (bind ?goal-block (nth$ ?i ?goal-stack))
      (if (not (find-block-in-stacks ?goal-block))
         then (bind ?matched FALSE)
      )
   )
   (return ?matched)
)

(deffunction find-block-in-stacks (?block)
   (bind ?found FALSE)
   (foreach ?stack (find-all-facts ((?f stack)) (eq ?f:blocks ?block))
      (bind ?found TRUE)
   )
   (return ?found)
)

(defrule pick-up
   ?h <- (hand empty)
   ?s <- (stack (blocks ?block1 $?rest))
   =>
   (assert (hand in-hand))
   (modify ?s (blocks $?rest))
   (retract ?h)
)

(defrule put-down
   ?h <- (hand in-hand)
   =>
   (assert (hand empty))
   (retract ?h)
)

(defrule stack
   ?h <- (hand empty)
   ?s

