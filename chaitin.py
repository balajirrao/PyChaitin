import itertools
import fol
from fol import Exists, Variable, Conjunction, AtomicFormula, Implies, Constant
from time import sleep
from  multiprocessing import Pool

pool = Pool(processes=1)

def output_f(p, n, y):
    """Predicate determining if a program p outputs y in less than or equal to n steps"""
    result = pool.apply_async(eval, (p,))
    if result.get(timeout=1) == y:
        return True
    else:
        return False


def is_nat_f(n):
    """Predicate determining if a string is a natural number"""
    return str.isdigit(n)


def length_greater_than_f(y, n):
    """Predicate determining if length of a string is less than n"""
    return (len(y) > n)


def constant_generator():
    i = 1
    allowed_chars = [chr(i) for i in range(255)]
    while True:
        iter = itertools.product(allowed_chars, repeat=i)
        for s in iter:
            yield s
        i = i + 1

outputs = fol.Predicate(output_f, 3)
is_nat = fol.Predicate(is_nat_f, 1)
lgt = fol.Predicate(length_greater_than_f, 2)

s = fol.system(constant_generator(), [])

for p in s.proofs():
    if type(p) == Implies and type(p.q) == AtomicFormula and p.q.predicate == lgt:
        prog = p.q.args[0]
        n = p.q.args[1]

        p1 = p.p
        if type(p1) == Conjunction and type(p1.q) == AtomicFormula and p1.q.predicate == outputs and p1.q.args[
                                                                                                     0] == prog:
            y = p1.q.args[1]

            if type(p1.p) == AtomicFormula and p1.p.predicate == is_nat and p1.p.args[0] == n:
                print y