;;DEFTEMPLATES USED*********
;;The primary templates used were father/mother-of, male/female while not using the husband/wife-of
;;The reasoning was that my focus was on identifying blood relatives and relatives married aren't necessarily related. If they were, that can be indicated in the family tree.
;;I also created some of my own deftemplates to essentially store the relationships without neccessarily needing to use it to infer further relationships, however, they may be required for a more developed tree
;;**************************

;CRITERIA*******************
;1)    given the following deftemplates for facts describing a family tree, (deftemplate father‐of (slot father) (slot child))
;(deftemplate mother‐of (slot mother) (slot child)) (deftemplate male (slot person))
;(deftemplate female (slot person)) (deftemplate wife‐of (slot wife) (slot husband))
;(deftemplate husband‐of (slot husband) (slot wife))
;
;write rules that infer the following relations. describe the deftemplates you use to solve the problem.
;
;a)    uncle, aunt
;b)    cousin
;c)    grandparent
;d)    grandfather, grandmother
;e)    sister, bother
;***************************

;defines facts and templates
(deftemplate father-of (slot father) (slot child))
(deftemplate mother-of (slot mother) (slot child)) (deftemplate male (slot person))
(deftemplate female (slot person)) 
(deftemplate wife-of (slot wife) (slot husband))
(deftemplate husband-of (slot husband) (slot wife))
;my templates
(deftemplate aunt (slot aunt) (slot niece-nephew))
(deftemplate uncle (slot uncle) (slot niece-nephew))
(deftemplate sister (slot sister) (slot sibling))
(deftemplate brother (slot brother) (slot sibling))
(deftemplate grandmother (slot grandmother) (slot grandkid))
(deftemplate grandfather (slot grandfather) (slot grandkid))
(deftemplate grandparent (slot grandparent) (slot grandkid))
(deftemplate cousin (slot cousin) (slot niece-neph))

(deffacts family
;parents
(father-of (father "dad") (child "son1"))
(mother-of (mother "mom") (child "son1"))
(male (person "dad")) (female (person "mom"))
(male (person "son1"))
(husband-of (husband "dad") (wife "mom"))
(wife-of (wife "mom") (husband "dad"))
;siblings
(father-of (father "dad") (child "son2"))
(mother-of (mother "mom") (child "son2"))
(father-of (father "dad") (child "daughter1"))
(mother-of (mother "mom") (child "daughter1"))
(male (person "son2")) (female (person "daughter1"))
;grandparents
(father-of (father "granddad1") (child "dad"))
(mother-of (mother "grandmom1") (child "dad"))
(father-of (father "granddad2") (child "mom"))
(mother-of (mother "grandmom2") (child "mom"))
(male (person "granddad1")) (female (person "grandmom1"))
(male (person "granddad2")) (female (person "grandmom2"))
(husband-of (husband "granddad1") (wife "grandmom1"))
(wife-of (wife "grandmom1") (husband "granddad1"))
(husband-of (husband "granddad2") (wife "grandmom2"))
(wife-of (wife "grandmom2") (husband "granddad2"))
;aunts-uncles
(father-of (father "granddad1") (child "aunt1"))
(mother-of (mother "grandmom1") (child "aunt1"))
(father-of (father "granddad2") (child "aunt2"))
(mother-of (mother "grandmom2") (child "aunt2"))
(father-of (father "granddad1") (child "aunt3"))
(mother-of (mother "grandmom1") (child "aunt3"))
(father-of (father "granddad2") (child "aunt4"))
(mother-of (mother "grandmom2") (child "aunt4"))
(father-of (father "granddad2") (child "uncle1"))
(mother-of (mother "grandmom2") (child "uncle1"))
(female (person "aunt1")) (female (person "aunt2"))
(female (person "aunt3")) (female (person "aunt4"))
(male (person "uncle1"))
(husband-of (husband "uncle1") (wife "aunt1"))
(wife-of (wife "aunt1") (husband "uncle1"))
;cousins
(mother-of (mother "aunt1") (child "cousin1"))
(mother-of (mother "aunt1") (child "cousin2"))
(father-of (father "uncle1") (child "cousin1"))
(father-of (father "uncle1") (child "cousin2"))
(male (person "cousin1")) (female (person "cousin2"))
)


;rules 			
(defrule aunt
	(father-of (father ?fa) (child ?name1))
	(father-of (father ?fa) (child ?name2&~?name1))
	(mother-of (mother ?mom) (child ?name1))
	(mother-of (mother ?mom) (child ?name2&~?name1))
	(or (father-of (father ?gfa) (child ?fa))
	    (father-of (father ?gfa) (child ?mom))
	)
	(father-of (father ?gfa) (child ?aunt&~?fa&~?mom))
	(or (mother-of (mother ?gmom) (child ?fa))
	    (mother-of (mother ?gmom) (child ?mom))
	)
	(mother-of (mother ?gmom) (child ?aunt&~?fa&~?mom))
	(female (person ?aunt))
	=>
	(printout t ?aunt " is the aunt of " ?name1 " and " ?name2 crlf)
	(assert (aunt (aunt ?aunt) (niece-nephew ?name2)))
	(assert (aunt (aunt ?aunt) (niece-nephew ?name1))))
	
(defrule uncle
	(father-of (father ?fa) (child ?name1))
	(father-of (father ?fa) (child ?name2&~?name1))
	(mother-of (mother ?mom) (child ?name1))
	(mother-of (mother ?mom) (child ?name2&~?name1))
	(or (father-of (father ?gfa) (child ?fa))
	    (father-of (father ?gfa) (child ?mom))
	)
	(father-of (father ?gfa) (child ?unc&~?fa&~?mom))
	(or (mother-of (mother ?gmom) (child ?fa))
	    (mother-of (mother ?gmom) (child ?mom))
	)
	(mother-of (mother ?gmom) (child ?unc&~?fa&~?mom))
	(male (person ?unc))
	=>
	(printout t ?unc " is the uncle of " ?name1 " and " ?name2 crlf)
	(assert (uncle (uncle ?unc) (niece-nephew ?name2)))
	(assert (uncle (uncle ?unc) (niece-nephew ?name1))))

(defrule cousin-a
    (father-of (father ?fa) (child ?name1))
	(mother-of (mother ?mom) (child ?name1))
	(or (father-of (father ?gfa) (child ?fa))
	    (father-of (father ?gfa) (child ?mom))
	)
	(father-of (father ?gfa) (child ?unc&~?fa&~?mom))
	(or (mother-of (mother ?gmom) (child ?fa))
	    (mother-of (mother ?gmom) (child ?mom))
	)
	(mother-of (mother ?gmom) (child ?unc&~?fa&~?mom))
	(male (person ?unc))
	(father-of (father ?unc) (child ?cousin))
  =>
  (assert (cousin (cousin ?cousin) (niece-neph ?name1)))
)

(defrule cousin-b
    (father-of (father ?fa) (child ?name1))
	(mother-of (mother ?mom) (child ?name1))
	(or (father-of (father ?gfa) (child ?fa))
	    (father-of (father ?gfa) (child ?mom))
	)
	(father-of (father ?gfa) (child ?aunt&~?fa&~?mom))
	(or (mother-of (mother ?gmom) (child ?fa))
	    (mother-of (mother ?gmom) (child ?mom))
	)
	(mother-of (mother ?gmom) (child ?aunt&~?fa&~?mom))
	(female (person ?unc))
	(father-of (father ?aunt) (child ?cousin))
  =>
  (assert (cousin (cousin ?cousin) (niece-neph ?name1)))
)


(defrule grandparent-a
  (father-of (father ?parent) (child ?grandc))
  (father-of (father ?grandparent) (child ?parent))
  =>
  (assert (grandparent (grandparent ?grandparent) (grandkid ?grandc)))
)

(defrule grandparent-b
  (mother-of (mother ?parent) (child ?grandc))
  (mother-of (mother ?grandparent) (child ?parent))
  =>
  (assert (grandparent (grandparent ?grandparent) (grandkid ?grandc)))
)


(defrule grandmother
	(father-of (father ?fa) (child ?name1))
	(father-of (father ?fa) (child ?name2&~?name1))
	(mother-of (mother ?mom) (child ?name1))
	(mother-of (mother ?mom) (child ?name2&~?name1))
	(or (mother-of (mother ?gmom) (child ?fa))
	(mother-of (mother ?gmom) (child ?mom))
	)
	(female (person ?gmom))
	=>
	(printout t ?gmom " is the grandmother of " ?name1 " and " ?name2 crlf)
	(assert (grandmother (grandmother ?gmom) (grandkid ?name2)))
	(assert (grandmother (grandmother ?gmom) (grandkid ?name1))))
	
(defrule grandfather
	(father-of (father ?fa) (child ?name1))
	(father-of (father ?fa) (child ?name2&~?name1))
	(mother-of (mother ?mom) (child ?name1))
	(mother-of (mother ?mom) (child ?name2&~?name1))
	(or (father-of (father ?gfa) (child ?fa))
	(father-of (father ?gfa) (child ?mom))
	)
	(male (person ?gfa))
	=>
	(printout t ?gfa " is the grandfather of " ?name1 " and " ?name2 crlf)
	(assert (grandfather (grandfather ?gfa) (grandkid ?name2)))
	(assert (grandfather (grandfather ?gfa) (grandkid ?name1))))


(defrule sister
	(father-of (father ?fa) (child ?name1))
	(father-of (father ?fa) (child ?name2&~?name1))
	(mother-of (mother ?mom) (child ?name1))
	(mother-of (mother ?mom) (child ?name2&~?name1))
	(female (person ?name2))
	=>
	(printout t ?name2 " is the sister of " ?name1 crlf)
	(assert (sister (sister ?name2) (sibling ?name1))))
	
(defrule brother
	(father-of (father ?fa) (child ?name1))
	(father-of (father ?fa) (child ?name2&~?name1))
	(mother-of (mother ?mom) (child ?name1))
	(mother-of (mother ?mom) (child ?name2&~?name1))
	(male (person ?name2))
	=>
	(printout t ?name2 " is the brother of " ?name1 crlf)
	(assert (brother (brother ?name2) (sibling ?name1))))

