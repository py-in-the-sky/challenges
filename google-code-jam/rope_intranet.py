"""
https://code.google.com/codejam/contest/619102/dashboard#s=p0
https://code.google.com/codejam/contest/619102/dashboard#s=a&a=0
"""


from bisect import bisect


def solve(wires):
    map_a = {w[0]: w for w in wires}
    map_b = {w[1]: w for w in wires}
    A = sorted(w[0] for w in wires)
    B = sorted(w[1] for w in wires)

    result = 0

    for wire in wires:
        a, b = wire
        # Find all intersections (a2, b2) where a < a2 and b > b2.
        # (Additionally counting the other way, where where a > a2 and b < b2,
        # would double-count each intersection.)
        A2, B2 = A[bisect(A, a):], B[:bisect(B, b)]
        crossed = set(map_a[a] for a in A2) & set(map_b[b] for b in B2)
        result += len(crossed)

    return result


def solve2(wires):
    """
    A brute-force O(N**2) solution is fine since O(N**2) is really at most
    (10**4)**2 = 10**8, or one-hundred-million comparisons.
    """
    result = 0

    for w1 in wires:
        for w2 in wires:
            result += int(w1[0] < w2[0] and w1[1] > w2[1])

    return result


def main():
    parse_wire = lambda line: tuple(map(int, line.split()))

    T = int(raw_input().strip())
    for t in xrange(1, T+1):
        N = int(raw_input().strip())
        wires = [parse_wire(raw_input().strip()) for _ in xrange(N)]
        print 'Case #{}: {}'.format(t, solve2(wires))


if __name__ == '__main__':
    main()
