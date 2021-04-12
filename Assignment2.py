#homework assignment for exam 2 grade, due 10/22/18 @ 9:00am
"""
1.	Given a sentence S = “Let us book that flight”,
how would you provide the corresponding POS tag sequence,
assuming that you need to disambiguate the word class of book? (50%)

2.	You need to develop the context-free grammar that can parse
 all the following sentences. You will use Python environment
 to test your grammar to make sure that it does the job
 and save your Python screenshot. (50%)

(a)	 “It was a nice party yesterday”
(b)	“She gave me that book two days ago”
(c)	“You said that”
(d)	“Please pass me this dish”

Besides these four sentences, list up to three different sentences that can be
parsed by this grammar as well as the corresponding Python screenshot.
Of the three sentences, can you generate one that does not make sense?
Why can’t you have such a sentence based on your grammar? (20%)
Now, assuming that the above four sentences are your mini-mini training corpus,
you will write a probabilistic context-free grammar.
You will use Python environments to test your grammar and
save the Python screenshot. (30%)
"""

import nltk
from nltk import *

sen1 = "it was a nice party yesterday".split()
sen2 = "she gave me that book two days ago".split()
sen3 = "you said that".split()
sen4 = "please pass me this dish".split()
sen5 = "she gave me this dish".split()
sen6 = "it was a nice dish".split()
sen7 =  "you gave me a nice party".split()

#TODO: look into Adj and Adv structures for this context
flight_grammar = nltk.CFG.fromstring("""
S -> NP VP | VP | NP
NP -> Prop | Det N | Det N PP | Det Adj N | Adj N | N Adv | Adj N Adv | Det Adj N Adv | N PP | N | N NP
VP -> V NP | V NP PP | V PP | V Adv | Adv V | Adv V NP | Adv V NP PP
PP -> P NP | P VP | P
N -> "party" | "days" | "me" | "dish" | "book"
Adj -> "nice" | "two"
Det -> "a" | "the"
Prop -> "she" | "you" | "it"
V -> "gave" | "said" | "pass" | "was"
P -> "that" | "this"
Adv -> "ago" | "please" | "yesterday"
""")

rd_parser = nltk.RecursiveDescentParser(flight_grammar)
tree1 = rd_parser.parse(sen1)
tree2 = rd_parser.parse(sen2)
tree3 = rd_parser.parse(sen3)
tree4 = rd_parser.parse(sen4)
tree5 = rd_parser.parse(sen5)
tree6 = rd_parser.parse(sen6)
tree7 = rd_parser.parse(sen7)

#When I ran this, I commented them out and ran them one by one so I could see when something went wrong
treelist = list(tree1)
treelist = list(tree2)
treelist = list(tree3)
treelist = list(tree4)
treelist = list(tree5)
treelist = list(tree6)
treelist = list(tree7)
for tree in treelist:
    print(tree)
