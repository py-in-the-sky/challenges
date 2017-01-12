
'''Finding the average of two very large numbers (a and b):

a + (b-a)/2 is preferable to (a+b)/2 and a/2 + b/2
because (a+b) may be larger than can be stored in
memory and hence produce an overflow and a/2 + b/2
will underestimate integer division in some
circumstances (e.g., a=3 and b=7).

This algorithm runs O(nlogn).
Solves the large input in 0.056 seconds, which is over
an order of magnitude faster than longest_increasing_subsequence_3.py,
which solves it in 0.99 seconds and runs O(n**2).

The bisect module implements an efficient binary search algorithm.

LIS references:
www.geeksforgeeks.org/longest-monotonically-increasing-subsequence-size-n-log-n/
www.cs.washington.edu/education/courses/cse417/02wi/slides/06dp-lis.pdf
en.wikipedia.org/wiki/Longest_increasing_subsequence
architects.dzone.com/articles/algorithm-week-longest
www.algorithmist.com/index.php/Longest_Increasing_Subsequence

practice input:
4
4
1 4 3 3
5
3 4 6 7 10
4
4 3 2 1
5
4 5 6 1 7

practice output:
Case #1: 2
Case #2: 0
Case #3: 3
Case #4: 1
'''


import bisect


def get_lis(p):  # lis = longest increasing subsequence
    '''(list of numbers) -> list of numbers

    Requirement: len(p) > 0 and p contains only numbers.
    Returns a strictly increasing subsequence of numbers (in reverse
    order, in this implementation) from p whose length is greater than
    or equal to all other strictly increasing subsequences of p.
    There is not necessarily one unique "longest" increasing subsequence
    of an arbitrary p.

    >>> get_lis([1,2,3])
    [3,2,1]
    >>> get_lis([4,5,6,10,9,20])
    [4,5,6,9,20]
    >>> get_lis([4,3,2,1])
    [1]
    '''
    subseqs = [[p[0]]]  # accumulates strictly increasing subsequences
    for e in p[1:]:
        elem = [e]
        insertion = bisect.bisect_left(subseqs, elem)
        if insertion == 0:
            subseqs[0] = elem
            continue
        nsubseqs = len(subseqs)
        if insertion == nsubseqs:
            subseqs.append(elem + subseqs[-1])
        elif 0 < insertion < nsubseqs:
            subseqs[insertion] = elem + subseqs[insertion-1]
    return subseqs[-1]


def get_lis_length(p):
    '''
    This is a more efficient version if what you're after is
    not a sequence but just the length of the lis.  It's more
    efficient because it keeps just a list of ints, instead of
    a list of lists.  The list of ints solution was discovered
    based on the insight that, in get_lis, all decisions on
    where to insert the current element into subseqs were based
    only on the last item in each list in subseqs.  Therefore,
    in this implementation, only the "last" item is held at each
    index in "subseqs", which has been renamed "ends" in this
    implementation.

    The run time for the solution on Google Code Jam's large
    input set was half that of get_lis's.
    '''
    ends = [p[0]]
    for e in p[1:]:
        insertion = bisect.bisect_left(ends, e)
        if insertion == 0:
            ends[0] = e
            continue
        num_ends = len(ends)
        if insertion == num_ends:
            ends.append(e)
        elif 0 < insertion < num_ends:
            ends[insertion] = e
    return len(ends)


def main():
    inputs = open('C-large-practice.in', 'r')
    inputs.readline()
    outputs = open('answer.out', 'w')
    case = 1
    while inputs.readline():
        houses = map(int, inputs.readline().strip().split())
        #answer = len(houses) - len(get_lis(houses))
        answer = len(houses) - get_lis_length(houses)
        # print 'Case #{}: {}'.format(case, answer)
        outputs.write('Case #{}: {}'.format(case, answer) + '\n')
        case += 1
    outputs.close()
    inputs.close()
    print 'done!'


if __name__ == '__main__':
    main()
