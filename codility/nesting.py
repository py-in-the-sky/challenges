"""
https://codility.com/programmers/task/nesting/
"""


def solution(S):
    balance = 0

    for char in S:
        balance += (1 if char == '(' else -1)

        if balance < 0:
            return 0

    return int(balance == 0)
