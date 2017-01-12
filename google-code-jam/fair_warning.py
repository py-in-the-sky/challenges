"""
https://code.google.com/codejam/contest/433101/dashboard#s=p1
"""

def gcd(a, b):
    if b > a:
        return gcd(b, a)
    elif b == 0:
        return a
    else:
        return gcd(b, a % b)


def big_gcd(a):
    return reduce(lambda x,y: gcd(x, y), a)


def solve(nums):
    nums = sorted(nums)
    diffs = [(nums[i] - nums[i-1]) for i in xrange(1, len(nums))]
    T = big_gcd(diffs)
    n = nums[0]
    return 0 if n % T == 0 else T - (n % T)


def main():
    C = int(raw_input())
    for c in xrange(1, C+1):
        nums = map(int, raw_input().strip().split())
        print 'Case #{}: {}'.format(c, solve(nums[1:]))


if __name__ == '__main__':
    main()
