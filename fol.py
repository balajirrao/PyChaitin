import itertools

class Term(object):
    def __init__(self):
        pass


class Variable(Term):
    def __init__(self, s=""):
        self._symbol = s


class Constant(Term):
    def __init__(self, s):
        pass


class Operation(Term):
    def __init__(self, function, degree, terms):
        self.f = function
        self.degree = degree
        self.terms = terms
        pass


class Formula(object):
    def __post_order(self, f):
        for child in f.children:
            for gr_child in child.__iter__():
                yield gr_child
        yield f

    def __iter__(self):
        return self.__post_order(self)

    def __init__(self, c=list()):
        self.children = list(c)


class Predicate:
    def __init__(self, function, degree):
        self.f = function
        self.degree = degree
        pass


class AtomicFormula(Formula):
    def __init__(self, predicate, args, c=list()):
        self.predicate = predicate
        self.args = args
        Formula.__init__(self, c)


class Implies(Formula):
    def __init__(self, p, q):
        Formula.__init__(self)
        self.p = p
        self.q = q


class Iff(Formula):
    def __init__(self, p, q):
        Formula.__init__(self)
        self.p = p
        self.q = q


class Conjunction(Formula):
    def __init__(self, p, q):
        Formula.__init__(self)
        self.p = p
        self.q = q


class Disjunction(Formula):
    def __init__(self, p, q):
        Formula.__init__(self)
        self.p = p
        self.q = q


class Negation(Formula):
    def __init__(self, p):
        Formula.__init__(self)
        self.p = p


class Forall(Formula):
    def __init__(self, x, p):
        Formula.__init__(self)
        self.x = x
        self.p = p


class Exists(Formula):
    def __init__(self, x, p):
        Formula.__init__(self)
        self.x = x
        self.p = p


tautologies = [lambda p, q: Implies(p, p),
               lambda p, q: Implies(p, Implies(q, p)),
               lambda p, q: Implies(Negation(Negation(p)), p),
               lambda p, q: Implies(p, Negation(Negation(p))),
               lambda p, q: Implies(Negation(p), Implies(p, q)),
               lambda p, q: Negation(Implies(p, Negation(q))),
               lambda p, q: Implies(Conjunction(p, q), Negation(Implies(p, Negation(q)))),
               lambda p, q: Implies(Negation(p), q),
               lambda p, q: Implies(Disjunction(p, q), Implies(Negation(p), q)),
               lambda p, q: Implies(p, Implies(Negation(q), Negation(Implies(p, q)))),
               lambda p, q: Implies(Implies(p, q), Implies(Implies(Negation(p), q), q)),
               lambda p, q: Implies(Implies(p, q), Implies(Negation(q), Negation(p))),
               lambda p, q: Implies(Implies(p, q), Implies(Implies(q, p), Disjunction(p, q))),
               lambda p, q: Implies(Disjunction(p, q), Implies(p, q)),
               lambda p, q: Implies(Disjunction(p, q), Implies(q, p)),
               lambda p, q: Implies(Implies(Negation(q), Negation(p)), Implies(Implies(Negation(q), p), q)),
               lambda p, q, r: Implies(Implies(p, Implies(q, r)), Implies(Implies(p, q), Implies(p, r))),
]

class system:
    def __init__(self, constants, axioms):
        self.constants = constants
        self.deduced_statements = list(axioms)
        self.null = Formula(self.deduced_statements)


    def introduce_tautologies(self):
        _new_deductions = list();

        for t in tautologies:
            iter = itertools.product(self.deduced_statements, t.__code__.co_argcount)
            for i in iter:
                _new_deductions.append(t(i))

        self.deduced_statements.append(_new_deductions)

    def proofs(self):
        while True:
            new_deductions = list()
            for d in self.deduced_statements:
                iter = self.null.__iter__()
                for i in iter:
                    if i.__class__ == Implies:
                        if i.p == d and i.q not in self.deduced_statements:
                            d.children.append(i.q)
                            i.children.append(i.q)
                            yield i.q
                            new_deductions.append(i.q)
                        self.introduce_tautologies()
            self.deduced_statements.extend(new_deductions)
            if len(new_deductions) == 0:
                break