"""
Use Catalan numbers to reason about and test the correctness of this algorithm.
In particular, the aspect of correctness that we're concerned about is the
algorithm's comprehensiveness -- does it indeed capture all distinct sets of
balanced parentheses with N pairs of parenthesis?

We expect explosive growth because we're taking the number of balanced parentheses
at level N-1 and roughly multiplying that by 3 (without controlling for duplicates,
we'd be multiplying by exactly 3).

The only place for possible duplication is bp3. Therefore, the number of sets of
balanced parentheses at level N is between 2 and 3 times that of level N-1. Therefore,
the number of parentheses at level N is in [2**N-1, 3**N-1].
"""


def all_balanced_parentheses(n):
    if n == 1:
        yield '()'
    else:
        seen = set()
        for bp in all_balanced_parentheses(n-1):
            bp1 = '(' + bp + ')'
            if bp1 not in seen:
                yield bp1
                seen.add(bp1)

            bp2 = '()' + bp
            if bp2 not in seen:
                yield bp2
                seen.add(bp2)

            bp3 = bp + '()'
            if bp3 not in seen:
                yield bp3
                seen.add(bp3)


def all_balanced_parentheses_alt(n):
    if n == 1:
        yield '()'
    else:
        seen = set()
        for bp in all_balanced_parentheses_alt(n-1):
            bp1 = '(' + bp + ')'
            yield bp1

            bp2 = '()' + bp
            yield bp2
            seen.add(bp2)

            bp3 = bp + '()'
            if bp3 not in seen:
                yield bp3
                seen.add(bp3)


def test():
    # test_fn = all_balanced_parentheses_alt
    test_fn = all_balanced_parentheses
    count = lambda gen: sum(1 for _ in gen)

    assert count(test_fn(1)) == 1
    assert count(test_fn(2)) == 2
    assert all(2**(n-1) < count(test_fn(n)) < 3**(n-1) for n in xrange(3, 15))

    # Test that all are distinct.
    cases = (list(test_fn(n)) for n in xrange(1, 11))
    assert all(len(c) == len(set(c)) for c in cases)

    print 'Tests pass!'


def main():
    N = int(raw_input().strip())
    for bp in all_balanced_parentheses(N):
        print bp


if __name__ == '__main__':
    # main()
    test()
