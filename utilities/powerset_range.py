"""
If you can index your N objects with the integers in [0, N), then you can use
the powerset_range function to generate a powerset for all your indexes.
"""


def powerset_range(N):
    "Powerset of all numbers in range [0, N)."
    bit_sets = range(2**N)
    return frozenset(frozenset(active_bits(n)) for n in bit_sets)


def active_bits(n):
    "Generator. Indices of all bits of n that are set to 1."
    return (i for i,bit in enumerate(bits(n)) if bit == 1)


def bits(n):
    "Generator. All bits of n, from least to most significant."
    while n > 0:
        yield n & 1
        n >>= 1
