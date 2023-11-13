(defrule one ;checks if both marks at beginning of string, removes them, stops
?id <- (fact # @ $?str)
=>
(retract ?id)
(assert (fact $?str))
(printout t "string reversed: " $?str crlf)
(halt))

(defrule two-one ;checks if mark1 is one char away from mark2. Moves mark2 one space left, mark1 at back at beginning
?id <- (fact $?str # ?char @ $?str2)
=>
(retract ?id)
(assert (fact # $?str @ ?char $?str2)))

(defrule two-two ;checks for mark1 inside the string not at beginning, moves mark right one space and swaps chars
?id <- (fact $?str # ?char1&~@ ?char2&~@ $?str2)
=>
(retract ?id)
(assert (fact $?str ?char2 # ?char1 $?str2)))

(defrule two-three ;looks for mark at beginning of string, moves right one space, swaps chars
?id <- (fact # ?char1&~@ ?char2&~@ $?str)
=>
(retract ?id)
(assert (fact ?char2 # ?char1 $?str)))

(defrule three
(not (fact # $?str @ ?char))
(not (fact $?str # $?str2 @ ?char))
?id <- (fact $?str @ ?char)
=>
(retract ?id)
(assert (fact # $?str @ ?char)))

(defrule four-one
(not (fact $?str # $?str2 @ $?str3))
?id <- (fact $?str @ ?char1 ?char2 $?str2)
=>
(retract ?id)
(assert (fact $?str ?char2 @ ?char1 $?str2)))

(defrule four-two
?id <- (fact ?char&~# @ ?char1 ?char2 $?str)
=>
(retract ?id)
(assert (fact ?char ?char2 @ ?char1 $?str)))

(defrule five
?id <- (fact @ ?char1 ?char2 $?str)
=>
(retract ?id)
(assert (fact ?char2 @ ?char1 $?str)))

(defrule six
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
