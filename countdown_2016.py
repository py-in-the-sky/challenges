"""
Slight adaptation of the solution from:
http://nbviewer.jupyter.org/url/norvig.com/ipython/Countdown.ipynb

This adaptation uses memoization instead of explicitly mutating a dictionary
of expressions.
"""


from itertools import product


C10 = (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)


def memo(f):
    """memoization decorator, taken from Peter Norvig's Design of Computer
    Programs course on Udacity.com"""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = cache[args] = f(*args)
            return result
        except TypeError:  # unhashable argument
            return f(*args)
    return _f


def splits(items):
    "Split sequence of items into two non-empty parts, in all ways."
    return [(items[:i], items[i:]) for i in range(1, len(items))]


@memo
def expressions(numbers):
    "Return dictionary of all value-expression pairs for `numbers` in a dict."
    if len(numbers) == 1:  # Only one way to make an expression out of a single number
        n = numbers[0]
        return {n: str(n)}

    _expressions = {}
    # Split in all ways; get tables for left and right; combine tables in all ways.
    for (Lnums, Rnums) in splits(numbers):
        for ((L, Lexp), (R, Rexp)) in product(expressions(Lnums).iteritems(), expressions(Rnums).iteritems()):
            Lexp, Rexp = '(' + Lexp, Rexp + ')'
            if R != 0:
                _expressions[L/R] = Lexp + '/' + Rexp
            _expressions[L*R] = Lexp + '*' + Rexp
            _expressions[L-R] = Lexp + '-' + Rexp
            _expressions[L+R] = Lexp + '+' + Rexp

    return _expressions


# eval(expressions(C10)[2016]) == 2016
