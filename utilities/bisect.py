def bisect_left(A, x):
    "Return leftmost index where you could insort x into A."
    lo, hi = 0, len(A)

    while lo < hi:
        # Loop invariant: lo <= the leftmost index where you could insort x
        # Loop invariant: hi >= the leftmost index where you could insort x
        mid = (hi + lo) // 2

        if A[mid] < x:
            # A[mid+1] is < x or is the leftmost value >= x
            lo = mid + 1
        else:
            hi = mid

    return lo


def bisect_right(A, x):
    "Return rightmost index where you could insort x into A."
    lo, hi = 0, len(A)

    while lo < hi:
        # Loop invariant: hi >= the rightmost index where you could insort x
        # Loop invariant: lo >= the rightmost index where you could insort x
        mid = (hi + lo) // 2

        if A[mid] > x:
            # A[mid-1] is > x or is the rightmost value <= x
            hi = mid
        else:
            lo = mid + 1

    return lo


def tests():
    assert bisect_left([1,2,2,3], 2) is 1
    assert bisect_right([1,2,2,3], 2) is 3
    assert bisect_left([1,2,3], 0) is 0
    assert bisect_right([1,2,3], 0) is 0
    assert bisect_left([1,2,3], 4) is 3
    assert bisect_right([1,2,3], 4) is 3

    print 'tests passed!'
