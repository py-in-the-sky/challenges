"""
https://code.google.com/codejam/contest/635101/dashboard#s=p0

This solution is a simple DATA STRUCTURES solution. It uses a tree to
simulate the process described in the problem statement and runs in time
linear of the number of bytes in the input file, which is asymptotically
optimal.
"""


from collections import defaultdict


ROOT_DIR = ''


def tree(): return defaultdict(tree)


def directories(path):
    for directory in path.split('/'):
        if directory != ROOT_DIR:
            yield directory


def file_fixit(existing, desired):
    result = 0
    file_system = tree()

    for path in existing:
        t = file_system
        for directory in directories(path):
            t = t[directory]

    for path in desired:
        t = file_system
        for directory in directories(path):
            if directory not in t:
                result += 1
            t = t[directory]

    return result


def main():
    T = int(input().strip())

    for t in range(1, T+1):
        N, M = map(int, input().strip().split())
        existing = (input().strip() for _ in range(N))
        desired  = (input().strip() for _ in range(M))
        print("Case #{}: {}".format(t, file_fixit(existing, desired)))


if __name__ == '__main__':
    main()
