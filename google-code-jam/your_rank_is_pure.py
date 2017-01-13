"""
https://code.google.com/codejam/contest/635101/dashboard#s=p2

This solution is an example of COUNTING and DYNAMIC PROGRAMMING.

n = 5
2 3 4 5
3 4 5
2 3 5
2 5
5

n = 6
2 3 4 5 6
2 3 4 6
2 4 5 6
2 3 6
3 4 6
3 5 6
2 6
6

n = 7
2 3 4 5 6 7
2 3 4 5 7
3 4 5 6 7
2 3 5 6 7
2 3 4 7
2 4 6 7
2 4 5 7
4 5 6 7
...
"""


import sys; sys.setrecursionlimit(5000)


MOD = 100003


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


@memo
def sets_between_count(delta, n_between):
    assert delta > n_between

    if n_between == 0:
        return 1  # Just the empty set.

    return sum(sets_between_count(d, n_between - 1)
               for d in  xrange(delta - 1, n_between - 1, -1))


@memo
def pure_subsets_count(n, rank):
    assert n >= 2

    if rank < 1:
        return 0
    elif n == 2:
        return 1 if rank == 1 else 0
    elif rank <= 2:
        return 1

    # If n is pure and its rank is rank, then rank must be pure.
    # There can be at most an n-rank difference between the rank of n and the rank of rank.
    # (And at least a difference of 1.)
    ranks_of_rank = xrange(rank - (n - rank), rank)
    return sum(pure_subsets_count(rank, r) * sets_between_count(n - rank, rank - r - 1) % MOD
               for r in ranks_of_rank)


def solution(n):
    ranks = xrange(1, n)
    return sum(pure_subsets_count(n, r) % MOD for r in ranks) % MOD


def main():
    T = int(raw_input().strip())
    for t in xrange(1, T+1):
        n = int(raw_input().strip())
        print 'Case #{}: {}'.format(t, solution(n))


if __name__ == '__main__':
    main()
