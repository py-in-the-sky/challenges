def mushroom_picker(A, k, m):
    """
    A is a map of mushroom quantities along a road.  A mushroom picker starts
    at position k and has m moves to collect as many mushrooms as possible.
    Return max number of mushrooms the mushroom picker can collect.
    """
    # https://codility.com/media/train/3-PrefixSums.pdf
    total = sum(A)
    pref = prefix_sums(A)
    suff = suffix_sums(A)
    result = 0

    slice_sum = lambda i, j: total - pref[i] - suff[j]

    for i in xrange(m+1):
        right_end = min(k + i, len(A) - 1)
        left_end = max(k - (m - 2*i), 0)
        result = max(result, slice_sum(left_end, right_end))

    return result


def prefix_sums(A):
    result = [0] * len(A)

    for i in xrange(1, len(A)):
        result[i] = result[i-1] + A[i-1]

    return result


def suffix_sums(A):
    result = [0] * len(A)

    for i in xrange(len(A)-2, -1, -1):
        result[i] = result[i+1] + A[i+1]

    return result
