"""
This solution was written after reading the editorial for:
https://www.hackerrank.com/contests/world-codesprint-8/challenges/prime-digit-sums

This dynamic-programming solution is reminiscent of my solution to the Google Code
Jam problem in welcome_to_code_jam.py.

CONCETPS

* Let S be a string that satisfies all three properties. Then the first three and four
  digits of S sum to a prime. If we want to tack one more digit d onto the front of S and
  still have it be valid, then the sum of the first two digits of S plus d must be prime, 
  the sum of the first three digits of S and d must be prime, and the sum of the first four 
  digits of S and d must be prime.
* Let f(abcd, N) be the number of valid N-digit strings whose four leftmost digits are abcd.
  a cannot be 0.
* For 1 <= N < 4, we can find the answer by brute force since N is small enough.
* Consider a fifth digit e. abcde is valid iff sum(a,b,c,d,e), sum(b,c,d,e), and sum(c,d,e)
  are all prime. Therefore, we have the recurrence relation:

  f(abcd, N) = sum(f(bcde, N-1)) for e in [0, 9] and sum(a,b,c,d,e), sum(b,c,d,e), sum(c,d,e) all prime

* Base case: f(abcd, 4) = 1 if abcd is valid. Otherwise, it's 0.


MODELLING AND DATA TYPES


IMPLEMENTATION DETAILS

* Due to limitations on recursion depth in Python, we must explicitly build a table rather than recursively
  call a memoized function.
"""


from math import sqrt
from array import array
from collections import defaultdict


MOD = 10**9 + 7


def is_prime(n):
    if  n < 2:
        return False
    elif n == 2 or n == 3:
        return True
    else:
        return not any(n % x == 0 for x in xrange(2, int(sqrt(n) + 1)))


def sum_digits(n): return sum(int(d) for d in str(n))


def build_transitions_table():
    "A mapping from valid four-suffixes to valid five-suffixes."
    fours = ('0' * (4 - len(str(n))) + str(n) 
             for n in xrange(10**4))
    valid_fours = (abcd 
                   for abcd in fours
                   if is_prime(sum_digits(abcd))
                   and is_prime(sum_digits(abcd[:3]))
                   and is_prime(sum_digits(abcd[1:])))
    transitions = {abcd: frozenset(abcd + str(e) for e in xrange(10))
                   for abcd in valid_fours}
    valid_transitions = {abcd: frozenset(abcde
                                         for abcde in fives
                                         # We know sum(abc), sum(bcd), and sum(abcd) are all prime.
                                         if is_prime(sum_digits(abcde))  # sum(abcde) is prime.
                                         and is_prime(sum_digits(abcde[1:]))  # sum(bcde) prime.
                                         and is_prime(sum_digits(abcde[2:])))  # sum(cde) prime.
                         for abcd,fives in transitions.iteritems()}
    return valid_transitions


def build_counts_table(N):
    transitions = build_transitions_table()

    counts = array('i', (0 for _ in xrange(N+1)))
    counts[1] = 9  # ??? From editorial. Shouldn't it be 4?
    counts[2] = 90  # ??? From editorial.
    counts[3] = sum(is_prime(sum_digits(n)) for n in xrange(10**2, 10**3))
    counts[4] = sum(abcd[0] != '0' for abcd in transitions)

    previous_level_counts = {abcd: (0 if abcd[0] == '0' else 1)
                             for abcd in transitions}

    for n in xrange(5, N+1):
        current_level_counts = defaultdict(int)

        for abcd,count in previous_level_counts.iteritems():
            for abcde in transitions[abcd]:
                bcde = abcde[1:]
                current_level_counts[bcde] += count
                current_level_counts[bcde] %= MOD

        counts[n] = sum(current_level_counts.itervalues()) % MOD
        previous_level_counts = current_level_counts

    return counts


def responses(queries):
    assert all(n > 0 for n in queries)

    N = max(queries)
    counts = build_counts_table(N)
    return (counts[n] for n in queries)


def main():
    Q = int(raw_input().strip())
    queries = tuple(int(raw_input().strip()) for _ in xrange(Q))

    for r in responses(queries):
        print r


if __name__ == '__main__':
    main()
