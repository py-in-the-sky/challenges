"""
WIP!!!!!!!!

https://code.google.com/codejam/contest/2434486/dashboard#s=p1

This problem involves GEOMETRY, COUNTING, PROBABILITY, and dealing with tricky
edge cases around feasibility and counting.
"""


from math import factorial
from bisect import bisect_right


def nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))


def count_interleave(l, r):
    """The number of ways you can interleave a left sequence of lenght l and a
    right sequence of lenght r, is equal to the number of ways you can choose
    r spots from the resulting sequence of length l+r. Counting all the ways you
    can choose r spots from the resulting sequence is like choosing the number of
    of ways sequence r gets merged into the overall sequence.

    For an intuition of "interleave," think about how cards are shuffled together.
    The left stack stays in its original order and the right stack does, too. However,
    the two stacks are merged into one whole stack.
    """
    return nCr(l + r, r)


def pyramids_within_limit(limit):
    pyr_size = side_len = 1

    while pyr_size <= limit:
        yield pyr_size, side_len
        side_len += 2
        pyr_size += (side_len * 2 - 1)


def probability_of_diamond_at(point, N, pyr_sizes, pyr_side_lens):
    x, y = point
    target_layer = y + abs(x) // 2
    next_layer = bisect_right(pyr_sizes, N)
    free_diamonds = N - pyr_sizes[next_layer - 1]

    if target_layer < next_layer:
        return 1.0
    elif target_layer > next_layer or free_diamonds < y + 1 or x == 0:
        return 0.0

    side_len = pyr_side_lens[next_layer - 1]
    L = free_diamonds - (side_len + 1)
    p_comp = 0

    for l in xrange(L+1 if L > 0 else 0, y+1):
        c = count_interleave(l, free_diamonds - l)
        p_comp += (c * 0.5**free_diamonds)

    if L > 0:
        for l in xrange(1, L+1):
            c = count_interleave(side_len, l)
            p_comp += (c * 0.5**(side_len + l))

    return 1 - p_comp


def main():
    LIMIT = 10**6
    pyr_sizes, pyr_side_lens = zip(*pyramids_within_limit(LIMIT))
    T = int(raw_input().strip())

    for t in xrange(1, T+1):
        N, X, Y = map(int, raw_input().strip().split())
        print 'Case #{}: {}'.format(t, probability_of_diamond_at((X, Y), N, pyr_sizes, pyr_side_lens))


if __name__ == '__main__':
    main()
