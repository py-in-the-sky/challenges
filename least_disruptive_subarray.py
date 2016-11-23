"""
https://www.youtube.com/watch?v=1wMBw38rAlw
"""


def least_disruptive_subarray(a, s):
    """Returns index of a at which the values of s can begin being substituted in,
    causing the least 'disruption' to a, where the measure of 'disruption' is
    (a - a') + (b - b') + ... for the length of s."""
    assert len(s) <= len(a)

    s_sum = sum(s)
    a_sum = sum(a[i] for i in xrange(len(s)))
    disruption = abs(a_sum - s_sum)
    index = 0

    for i in xrange(len(s), len(a)):
        a_sum += (a[i] - a[i - len(s)])

        if abs(a_sum - s_sum) < disruption:
            index = i - len(s) + 1
            disruption = abs(a_sum - s_sum)

    return index
