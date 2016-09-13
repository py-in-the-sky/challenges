"""
https://codility.com/programmers/task/binary_gap/
"""


from math import log


def bits(n):
    "Yield bits from left to right."
    n_bits = int(log(n, 2)) + 1
    # The number of bits needed to represent a positive integer n

    for bit_shift in reversed(xrange(n_bits)):
        yield (n >> bit_shift) & 1


def solution(N):
    max_gap_len = 0
    current_gap_len = 0

    for bit in bits(N):  # time: O(log(N)); space: O(1)
        if bit == 1:
            max_gap_len = max(max_gap_len, current_gap_len)
            current_gap_len = 0
        else:
            current_gap_len += 1

    return max_gap_len
