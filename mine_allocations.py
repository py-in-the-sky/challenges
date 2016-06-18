"""
Greedy Algorithm

https://community.topcoder.com/stat?c=problem_statement&pm=1957&rd=4650
Discussion: https://www.topcoder.com/community/data-science/data-science-tutorials/greedy-is-good/

"[T]he profit of allocating an extra worker to a mine is always higher or equal
with the profit of allocating the next extra worker to that mine."  That is,
for each mine, the profit from allocating an additional miner is a non-increasing
sequence; the profit you'll get from adding this miner is greater than or
equal to the profit from allocating the next.

Because of this structure, we can devise a greedy algorithm that finds the
globally maximum profit.
"""


from collections import deque


def P_at_least_n(n, probabilities):
    return sum(probabilities[n:])


def get_marginal_profits(mine):
    probabilities = map(lambda f: f / 100, map(float, mine.split(', ')))
    mine_len = len(probabilities)
    marignal_probabilities = [P_at_least_n(n, probabilities) for n in xrange(mine_len)]

    mp = marignal_probabilities + [0]
    p = probabilities
    marginal_profits = (mp[i+1] * 60 + p[i] * (50 - 10*(i-1)) + (1 - mp[i]) * -20 for i in xrange(mine_len))

    marginal_profits = deque(marginal_profits)
    marginal_profits.popleft()  # remove p_0, which is always 1.0 and not needed for allocation decisions
    return marginal_profits


def get_allocation(mines, miners):
    marginal_profits = map(get_marginal_profits, mines)
    allocation = [0] * len(mines)

    for _ in xrange(miners):
        available_mines = (i for i,_ in  enumerate(marginal_profits) if allocation[i] < 6)
        i = max(available_mines, key=lambda i: marginal_profits[i][0])
        mine = marginal_profits[i]
        mine.popleft()  # remove marginal profit from used allocation
        allocation[i] += 1

    return allocation


def tests():
    miners = 4
    mines = [
        "000, 030, 030, 040, 000, 000, 000",
        "020, 020, 020, 010, 010, 010, 010"
    ]
    assert get_allocation(mines, miners) == [2, 2]
    print 'one'

    miners = 8
    mines = [
        "100, 000, 000, 000, 000, 000, 000",
        "100, 000, 000, 000, 000, 000, 000",
        "100, 000, 000, 000, 000, 000, 000",
        "100, 000, 000, 000, 000, 000, 000",
        "100, 000, 000, 000, 000, 000, 000"
    ]
    assert get_allocation(mines, miners) == [6,  2,  0,  0,  0]
    print 'two'

    miners = 30
    mines = [
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000",
        "050, 000, 000, 000, 000, 050, 000"
    ]
    assert get_allocation(mines, miners) == [4,  4,  4,  4,  4,  4,  4,  2,  0,  0]
    print 'three'

    miners = 56
    mines = [
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004",
        "026, 012, 005, 013, 038, 002, 004"
    ]
    assert get_allocation(mines, miners) == [2,  2,  2,  2,  2,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]
    print 'four'

    miners = 150
    mines = [
        "100, 000, 000, 000, 000, 000, 000",
        "090, 010, 000, 000, 000, 000, 000",
        "080, 020, 000, 000, 000, 000, 000",
        "075, 025, 000, 000, 000, 000, 000",
        "050, 050, 000, 000, 000, 000, 000",
        "025, 075, 000, 000, 000, 000, 000",
        "020, 080, 000, 000, 000, 000, 000",
        "010, 090, 000, 000, 000, 000, 000",
        "000, 100, 000, 000, 000, 000, 000",
        "000, 090, 010, 000, 000, 000, 000",
        "000, 080, 020, 000, 000, 000, 000",
        "000, 075, 025, 000, 000, 000, 000",
        "000, 050, 050, 000, 000, 000, 000",
        "000, 025, 075, 000, 000, 000, 000",
        "000, 020, 080, 000, 000, 000, 000",
        "000, 010, 090, 000, 000, 000, 000",
        "000, 000, 100, 000, 000, 000, 000",
        "000, 000, 090, 010, 000, 000, 000",
        "000, 000, 080, 020, 000, 000, 000",
        "000, 000, 075, 025, 000, 000, 000",
        "000, 000, 050, 050, 000, 000, 000",
        "000, 000, 025, 075, 000, 000, 000",
        "000, 000, 020, 080, 000, 000, 000",
        "000, 000, 010, 090, 000, 000, 000",
        "000, 000, 000, 100, 000, 000, 000",
        "000, 000, 000, 100, 000, 000, 000",
        "000, 000, 000, 090, 010, 000, 000",
        "000, 000, 000, 080, 020, 000, 000",
        "000, 000, 000, 075, 025, 000, 000",
        "000, 000, 000, 050, 050, 000, 000",
        "000, 000, 000, 025, 075, 000, 000",
        "000, 000, 000, 020, 080, 000, 000",
        "000, 000, 000, 010, 090, 000, 000",
        "000, 000, 000, 000, 100, 000, 000",
        "000, 000, 000, 000, 090, 010, 000",
        "000, 000, 000, 000, 080, 020, 000",
        "000, 000, 000, 000, 075, 025, 000",
        "000, 000, 000, 000, 050, 050, 000",
        "000, 000, 000, 000, 025, 075, 000",
        "000, 000, 000, 000, 020, 080, 000",
        "000, 000, 000, 000, 010, 090, 000",
        "000, 000, 000, 000, 000, 100, 000",
        "000, 000, 000, 000, 000, 090, 010",
        "000, 000, 000, 000, 000, 080, 020",
        "000, 000, 000, 000, 000, 075, 025",
        "000, 000, 000, 000, 000, 050, 050",
        "000, 000, 000, 000, 000, 025, 075",
        "000, 000, 000, 000, 000, 020, 080",
        "000, 000, 000, 000, 000, 010, 090",
        "000, 000, 000, 000, 000, 000, 100"
    ]
    assert get_allocation(mines, miners) == [0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  4,  4,  4,  4,  5,  5,  5,  5,  5,  5,  5,  5,  5,  5,  6,  6]
    print 'five'

    print 'tests pass!'


if __name__ == '__main__':
    tests()
