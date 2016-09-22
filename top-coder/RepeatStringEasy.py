"""
Single Round Match 698 Sponsored by Google (17 Sept 2016)

https://arena.topcoder.com/#/u/practiceCode/16811/53337/14390/2/329254
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
                lcs = max(lcs, lcs_candidate, key=_sequence_order_key)

        return lcs

    def _sequence_order_key(seq):
        "Longer sequence wins.  Ties go to the lexicographically larger sequence."
        return (len(seq), seq)

    return _loop(0, 0)


def solution(s):
    if len(s) <= 1:
        return 0

    return max(len(longest_common_subsequence(s[:i], s[i:])) * 2 for i in xrange(len(s)))


class RepeatStringEasy:
    def maximalLength(self, s):
        return solution(s)
