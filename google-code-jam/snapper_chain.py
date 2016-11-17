"""
https://code.google.com/codejam/contest/433101/dashboard
"""


def light_on(n, k):
    bits = bin(k)[2:]

    if len(bits) < n:
        return False

    return all(b == '1' for b in list(reversed(bits))[:n])


def main():
    T = int(raw_input())
    for t in xrange(1, T+1):
        n, k = map(int, raw_input().strip().split())
        print 'Case #{}: {}'.format(t, 'ON' if light_on(n, k) else 'OFF')


if __name__ == '__main__':
    main()
