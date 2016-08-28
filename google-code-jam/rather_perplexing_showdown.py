"""
https://code.google.com/codejam/contest/10224486/dashboard

Build tree from bottom up w/ X as winner.

Return lexicographically smallest lineup or 'IMPOSSIBLE'.

R beats S
S beats P
P beats R
"""


def count_chars(lineup):
    P = sum(char == 'P' for char in lineup)
    R = sum(char == 'R' for char in lineup)
    S = sum(char == 'S' for char in lineup)
    return (P, R, S)


def construct_table(N):
    mapping = {'P': 0, 'R': 1, 'S': 2}
    table = {
        0: ['P',  'R',  'S'],
        1: ['PR', 'RS', 'PS']
    }

    for n in xrange(2, N+1):
        table[n] = [None, None, None]
        for i in xrange(3):
            prev_entry = table[n-1][i]
            prev_half1, prev_half2 = prev_entry[:len(prev_entry) / 2], prev_entry[len(prev_entry) / 2:]
            idx1 = next(i for i,e in enumerate(table[n-2]) if e == prev_half1)
            idx2 = next(i for i,e in enumerate(table[n-2]) if e == prev_half2)
            next_half1, next_half2 = table[n-1][idx1], table[n-1][idx2]
            table[n][i] = ''.join(sorted([next_half1, next_half2]))

    for n,lineups in table.iteritems():
        table[n] = {count_chars(lineup): lineup for lineup in lineups}

    return table


def main():
    # table = construct_table(3)  # small input
    table = construct_table(12)  # large input
    T = int(raw_input().strip())
    for t in xrange(1, T+1):
        N, R, P, S = [int(n) for n in raw_input().strip().split()]
        print 'Case #{}: {}'.format(t, table[N].get((P, R, S), 'IMPOSSIBLE'))


if __name__ == '__main__':
    main()
