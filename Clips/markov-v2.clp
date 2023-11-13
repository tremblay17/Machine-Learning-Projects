(defrule one ;checks if both marks at beginning of string, removes them, stops
?id <- (fact # @ $?str)
=>
(retract ?id)
(assert (fact $?str))
(printout t "string reversed: " $?str crlf)
(halt))

(defrule two ;checks for mark in string, moves mark right one space and swaps chars
?id <- (fact $?str # ?char1 ?char2 $?str2)
=>
(retract ?id)
(if(eq ?char2 @)
then (assert (fact # $?str ?char2 ?char1 $?str2)) ;if the marks are one char separated, move mark on right one space left, mark on left back to beginning
else (if(and (not (eq ?char2 @))(not (eq ?char1 @)))
then (assert (fact $?str ?char2 # ?char1 $?str2))
else (assert (fact $?str ?char1 ?char2 $?str2))))
)

(defrule three ;matches only if @ mark is next to last char, adds new mark
(not (fact # $?str @ ?char))
(not (fact $?str # $?str2 @ ?char))
?id <- (fact $?str @ ?char)
=>
(retract ?id)
(assert (fact # $?str @ ?char)))

(defrule four ;looks for mark moves one space right, swaps chars
(not (fact $?str # $?str2 @ $?str3))
?id <- (fact $?str ?m&@|# ?char1 ?char2&~@&~# $?str2)
=>
(retract ?id)
(assert (fact $?str ?char2 ?m ?char1 $?str2)))

(defrule five ;matches fact containing no markers, adds @ mark
(and
    (not(fact @ $?str))
    (not(fact # $?str))
    (not(fact $?str @ $?str2))
    (not(fact $?str # $?str2))
)
?id <- (fact $?str)
=>
(retract ?id)
(assert (fact @ $?str))
)
