"""
Find an equilibrium of an array A of integers.

An equilibrium is an index i such that:

    sum(A[:i]) == sum(A[i+1:])


Notes:
* Knowing this can be solved in O(N) helps in coming up
  with a creative solution by giving you the confidence to
  know that a linear-time solution is possible.  How can
  one get this creative confidence when the worst-case
  running time is not known in advance?  Ask yourself if
  you can do better, if a simpler solutuion with a better
  running time can be done.
* The third pass is superior to the second because it deals just
  with the properties of sums and integers, not bothering with
  the construction of arrays.
* The second-pass solution (above) is better for two reasons:

    1. it builds only two arrays, whereas the allocation of
       new arrays in `reduce` below turns the first-pass solution
       into an O(N^2) solution

    2. before writing it, I asked whether the two ends of the array
       (index 0 and index len(A)-1) are valid candidates for
       equilibrium points, and it turns out they are (the first-pass
       solution below just assumes they're not since there's
       nothing to the left and right of them, respectively, but
       really we should say the sum is 0 if it does not involve
       any integers)
"""


# THIRD PASS

def solution(A):
    overall_sum = sum(A)
    left_sum = 0

    for i,a in enumerate(A):
        right_sum = overall_sum - left_sum - a
        if right_sum == left_sum:
            return i
        else:
            left_sum += a

    return -1


### SECOND PASS

def solution(A):
    prefix_sums = [None] * len(A)
    suffix_sums = [None] * len(A)

    p_sum = lambda i: 0 if (i == 0) else prefix_sums[i-1]
    s_sum = lambda i: 0 if (i == len(A) - 1) else suffix_sums[i+1]

    for i in xrange(len(A)):
        prefix_sums[i] = p_sum(i) + A[i]

    for i in reversed(xrange(len(A))):
        suffix_sums[i] = s_sum(i) + A[i]

    equilibria = (i for i in xrange(len(A)) if p_sum(i) == s_sum(i))
    return next(equilibria, -1)


### FIRST PASS

def prefix_sums(A):
    return reduce(lambda acc, x: acc + [x + acc[-1]], A, [0])


def solution(A):
    pre_sums = prefix_sums(A)
    suf_sums = list(reversed(prefix_sums(reversed(A))))[1:]
    return next((i for i in xrange(1, len(A)-1) if pre_sums[i] == suf_sums[i]), -1)


### TESTS

def tests():
  assert solution([-1, 3, -4, 5, 1, -6, 2, 1]) == 1

  print 'tests pass!'
