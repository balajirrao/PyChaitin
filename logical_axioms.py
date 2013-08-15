# -*- coding: utf8 -*-
from pyparsing import Literal, Word, ZeroOrMore, Forward, alphas, oneOf, Group, operatorPrecedence, replaceWith

def Syntax():
    imp = Literal(u'⇒').setParseAction(replaceWith("Implies"))
    conj = Literal(u'∧').setParseAction(replaceWith("Conjunction"))
    disj = Literal(u'∨').setParseAction(replaceWith("Disjunction"))
    iff = Literal(u'⇔').setParseAction(replaceWith("Disjunction"))

    #op = oneOf(u'⇒ ∧')
    op = imp | conj | disj | iff
    lpar = Literal('(').suppress()
    rpar = Literal(')').suppress()
    neg = Literal(u'¬').setParseAction(replaceWith("Negation"))
    prop = Word(u"pqr")
    expr = Forward()
    atom = prop | Group(lpar + expr + rpar)
    expr << ((atom + ZeroOrMore(op + expr)) | Group(neg + expr))

    return expr

s = [u"P ⇒ P",
     u"P ⇒ (Q ⇒ P)",
     u"(P ⇒ (Q ⇒ R)) ⇒ ((P ⇒ Q) ⇒ (P ⇒ R))",
     u"(¬(¬P)) ⇒ P",
     u"P ⇒ (¬(¬P))",
     u"(¬P) ⇒ (P ⇒ Q)",
     u"¬(P ⇒ (¬Q))) ⇒ (P ∧ Q)",
     u"(P ∧ Q) ⇒ (¬(P ⇒ (¬Q)))",
     u"(¬P) ⇒ Q) ⇒ (P ∨ Q)",
     u"(P ∨ Q) ⇒ ((¬P) ⇒ Q)",
     u"P ⇒ ((¬Q) ⇒ (¬(P ⇒ Q)))",
     u"(P ⇒ Q) ⇒ (((¬P) ⇒ Q) ⇒ Q)",
     u"(P ⇒ Q) ⇒ ((¬Q) ⇒ (¬P))",
     u"(P ⇒ Q) ⇒ ((Q ⇒ P) ⇒ (P ⇔ Q))",
     u"(P ⇔ Q) ⇒ (P ⇒ Q)",
     u"(P ⇔ Q) ⇒ (Q ⇒ P)",
     u"((¬Q) ⇒ (¬P)) ⇒ (((¬Q) ⇒ P) ⇒ Q)",
]

def f(x):
    if len(x) == 1:
        if  x[0].__class__ == unicode:
            return x[0]
        else:
            return f(x[0])
    elif len(x) == 2:
        return "Negation (" + f(x[1]) + ")"
    elif len(x) == 3:
        return x[1] + " (" + f(x[0]) + "," + f(x[2]) + ")"

expr = Syntax()

for string in s:
    w = expr.parseString(string.lower())
    print "lambda p,q : " + f(w) + ","


