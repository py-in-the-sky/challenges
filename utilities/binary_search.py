"""
Algorithm always finishes since each iteration shrinks (hi - lo).

Algorithm terminates when x has been found or when lo == mid == hi, just after
you've checked A[mid].

Loop invariants (what's true when you enter a loop):
    * lo < hi
    * lo <= mid
    * lo is <= the leftmost index where you'd insort x
    * hi is >= the rightmost index where you'd insort x
    * Therefore, if x is in A, then x is in A[lo:hi]; if x is not in A[lo:hi],
      then x is not in A

Terminating conditions of each loop (if different from loop invariants):
    * lo <= hi
"""


def binary_search(A, x):
    "Given an array A, sorted in ascending order, return the index of x in A or None."
    lo, hi = 0, len(A)
    mid = (lo + hi) // 2

    while lo < hi:
        if A[mid] == x:
            return mid
        elif A[mid] < x:
            lo = mid + 1
        else:
            hi = mid

        mid = (lo + hi) // 2

    return None


def tests():
    assert binary_search([], 1) is None
    assert binary_search([1,2,3], 4) is None
    assert binary_search([1,2,3], 0) is None
    assert binary_search([1,2,3], 3) is 2
    assert binary_search([1,3,4,5], 2) is None
    assert binary_search([1,2,4,5], 3) is None
    assert binary_search([1,2], 2) is 1
    assert binary_search([1,2], 1) is 0
    assert binary_search([1,2,2,3], 2) in (1,2)

    print 'tests pass!'


def binary_search_alt(A, x):
    "Given an array A, sorted in ascending order, return the index of x in A or None."
    lo, hi = 0, len(A) - 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if A[mid] == x:
            return mid
        elif A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1

    return None
