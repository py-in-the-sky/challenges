"""
https://www.facebook.com/hackercup/problem/1525154397757404/
https://www.facebook.com/notes/1264355396913692

Moves
    Append letter to end
    Subtract letter from end
    Print word

Goal
    Choose K of the N words to print, and their order, in order to
    minimize number of moves.

Method
    To write word B after word A is already written, subtract letters
    back to the longest common prefix between A and B, and then append
    letters in order to complete B.

    In order to get an optimal-subproblem structure, sort words
    lexicographically so that neighboring words have long common
    prefixes.
"""


INFINITY = float('inf')


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


def min_moves(words, K):
    words = sorted(words)

    def _min_moves(i, j):
        w1, w2 = words[i], words[j]
        max_common_prefix_len = 0

        for char1,char2 in zip(w1, w2):
            if char1 != char2:
                break
            max_common_prefix_len += 1

        return len(w1) + len(w2) - 2*max_common_prefix_len

    @memo
    def _lookup(i, k):
        if k == 1:  # type word and print it
            return len(words[i]) + 1
        # elif i == len(words) - 1:
        elif len(words) - i < k:  # not enough words to spare
            return INFINITY
        else:
            return min(_min_moves(i, j) + _lookup(j, k-1) + 1 for j in xrange(i+1, len(words)))

    return min(len(w) + _lookup(i, K) for i,w in enumerate(words))


def main():
    T = int(raw_input().strip())

    for t in xrange(1, T+1):
        N, K = map(int, raw_input().strip().split())
        words = [raw_input().strip() for _ in xrange(N)]
        print 'Case #{}: {}'.format(t, min_moves(words, K))


if __name__ == '__main__':
    main()
