from math import log


def bits_from_left(n):
    "Yield bits from right to left."
    # time: O(log(n)); space: O(1)

    n_bits = int(log(n, 2)) + 1
    # The number of bits needed to represent a positive integer n

    for _ in xrange(n_bits):
        yield n & 1
        n >>= 1


def bits_from_right(n):
    "Yield bits from left to right."
    # time: O(log(n)); space: O(1)

    n_bits = int(log(n, 2)) + 1
    # The number of bits needed to represent a positive integer n

    for bit_shift in reversed(xrange(n_bits)):
        yield (n >> bit_shift) & 1


bits = bits_from_right
