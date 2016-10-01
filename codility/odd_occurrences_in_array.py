"""
https://codility.com/programmers/task/odd_occurrences_in_array/
"""


from operator import xor


def solution(A):
    return reduce(xor, A, 0)
