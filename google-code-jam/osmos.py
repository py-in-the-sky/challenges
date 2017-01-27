"""
https://code.google.com/codejam/contest/dashboard?c=2434486

This is a SEARCH plus GREEDY ALGORITHM solution.

Specifically, it performs brute-force search over len(motes)+1 applications of the
greedy algorithm. The application of the greedy algorithm to larger problems is built
on solutions to smaller ones, so in one pass we memoize all results for 0..len(motes)+1,
storing the results in an array of length len(motes)+1, in O(len(motes)) time.

When removing a mote, it's always optimal to remove the largest remaining mote.

After removing the i largest motes, it's optimal to eat the rest greedily:
that is, eat them smallest-to-largest, and when you're not large enough to eat
the next mote in line, insert the largest mote you can eat (your current size minus 1).

After choosing i, how many of the largest motes to remove, the number of mote insertions
is determined by the greedy algorithm. Therefore, choose i from [0, N] such that
i plus the number of resulting greedy insertions is minimized.

Intuition: given that we're going to remove i motes:
    * Which i motes should we remove? It is optimal to remove the i largest.
    * How should we go about eating the rest? In the greedy fashion described above.
Given this, we choose the i that results in the fewest removals plus insertions.

See a more thorough justification of the greedy approach here:
https://code.google.com/codejam/contest/dashboard?c=2434486#s=a&a=0

Runtime: O(NlogN + NM/a) where M is the size of the largest mote.

Question: is the runtime pseudo-polynomial? It depends on the size of a, and for each
iteration in the main for loop, it performs operations on a. Therefore, in the runtime,
should we consider the size of the bit array that stores a?

No, it is not pseudo-polynomial. The analysis of pseudo-polynomial runtime proceeds by
expressing the input size in terms of the bits used, recasting the runtime expression
in terms of bits, and seeing whether the variables in the input expression are involved
in an exponential expression in the runtime.

    Input size: O(b + Nc) where b = O(loga) and c = O(logM).
    Runtime: O(NlogN + NM/a) = O(NlogN + N 2^c/2^b) = O(NlogN + N2^(c-b)).

Presumably, the number of bits to represent the integers a and M are the same, whether on
a 32- or 64-bit machine. Therefore, c-b doesn't change across these machines. Therefore,
this solution is not pseudo-polynomial; in other words, it's not exponential in any
input size.

See this as an informative example of pseudo-polynomial runtime analysis:
    https://courses.csail.mit.edu/6.006/fall11/rec/rec21_knapsack.pdf
"""


def osmos(a, motes):
    N = len(motes)

    if a == 1:  # a is not big enough to eat any motes and it therefore cannot grow.
        return N  # Just remove all motes.

    motes = sorted(motes)  # O(NlogN).
    n_intervening_motes = [0 for _ in xrange(N+1)]  # O(N).
    # n_intervening_motes: the number of motes greedily inserted when eating up to i motes.

    for i in xrange(1, N+1):  # O(NM/a) where M is the size of the largest mote.
        n = 0
        m = motes[i-1]

        while a <= m:
            a += a-1
            n += 1

        a += m
        n_intervening_motes[i] = n_intervening_motes[i-1] + n

    # Which produced the fewest removals plus inserts?
    return min(i + n_intervening_motes[N-i] for i in xrange(N+1))  # O(N).


def main():
    T = int(raw_input().strip())

    for t in xrange(1, T+1):
        A, N = map(int, raw_input().strip().split())
        motes = map(int, raw_input().strip().split())
        print 'Case #{}: {}'.format(t, osmos(A, motes))


if __name__ == '__main__':
    main()
