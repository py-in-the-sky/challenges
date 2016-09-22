"""
https://code.google.com/codejam/contest/32014/dashboard#s=p1
"""


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


def sequence_order(seq):
    "Longer sequence wins.  Ties go to the lexicographically larger sequence."
    return (len(seq), seq)


def longest_common_subsequence(a, b):
    "Return lexicographically largest longest common subsequence."

    @memo
    def _loop(i, j):
        if i >= len(a) or j >= len(b):
            return ()

        lcs = _loop(i+1, j)

        for j2 in xrange(j, len(b)):
            if a[i] == b[j2]:
                lcs_candidate = (a[i],) + _loop(i+1, j2+1)
                lcs = max(lcs, lcs_candidate, key=sequence_order)

        return lcs

    return _loop(0, 0)


# def price_is_wrong(ordering, guesses):
#     my_ordering = tuple(product for _,product in sorted(zip(guesses, ordering)))
#     lcs = longest_common_subsequence(ordering, my_ordering)
#     return sorted(product for product in ordering if product not in lcs)


def longest_increasing_subsequence(ordering, guesses):
    "Return lexicographically largest longest increasing subsequence."

    mapping = dict(zip(ordering, guesses))
    increasing_sequences = [(product,) for product in ordering]

    for i in xrange(1, len(increasing_sequences)):
        suffix = increasing_sequences[i]

        for j in xrange(0, i):
            prefix = increasing_sequences[j]

            if mapping[prefix[-1]] < mapping[suffix[0]]:
                increasing_sequences[i] = max(increasing_sequences[i], prefix + suffix, key=sequence_order)

    return max(increasing_sequences, key=sequence_order)


def price_is_wrong(ordering, guesses):
    lis = set(longest_increasing_subsequence(ordering, guesses))
    return sorted(product for product in ordering if product not in lis)


def main():
    T = int(raw_input().strip())

    for t in xrange(1, T+1):
        ordering = tuple(raw_input().strip().split())
        guesses = tuple(map(int, raw_input().strip().split()))
        result = ' '.join(price_is_wrong(ordering, guesses))
        print 'Case #{}: {}'.format(t, result)


if __name__ == '__main__':
    main()
