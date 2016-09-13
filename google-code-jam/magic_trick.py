"""
https://code.google.com/codejam/contest/2974486/dashboard
"""


def solve(ans1, ans2, cards1, cards2):
    row1 = frozenset(cards1[ans1 - 1])
    row2 = frozenset(cards2[ans2 - 1])
    intersection = row1 & row2

    if len(intersection) == 1:
        return str(next(e for e in intersection))
    elif len(intersection) == 0:
        return 'Volunteer cheated!'
    else:
        return 'Bad magician!'


def main():
    T = int(raw_input().strip())
    for t in xrange(1, T+1):
        ans1 = int(raw_input().strip())
        cards1 = [map(int, raw_input().strip().split()) for _ in xrange(4)]
        ans2 = int(raw_input().strip())
        cards2 = [map(int, raw_input().strip().split()) for _ in xrange(4)]
        print "Case #{}: {}".format(t, solve(ans1, ans2, cards1, cards2))


if __name__ == '__main__':
    main()
