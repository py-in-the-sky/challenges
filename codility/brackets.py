"""
https://codility.com/programmers/task/brackets/
"""


from collections import deque


def solution(S):
    q = deque()

    for char in S:
        if char in ')]}':
            if q and are_mirrors(char, q[-1]):
                q.pop()
            else:
                return 0
        else:
            q.append(char)

    return int(len(q) == 0)


def are_mirrors(source, target):
    if source == ')':
        return target == '('
    elif source == ']':
        return target == '['
    else:
        return target == '{'
