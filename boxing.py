"""
Greedy Algorithm

https://community.topcoder.com/stat?c=problem_statement&pm=2977&rd=5880

Timestamps are in milliseconds.
"""



from collections import deque


def max_credit(a, b, c, d, e):
    times = tuple(deque(t) for t in (a, b, c, d, e) if t)
    last_hit_at = 0
    n_hits = 0

    while sum(len(t) > 0 for t in times) >= 3:
        first, _, third = sorted(t[0] for t in times)[:3]
        if third - first <= 1000:
            n_hits += 1
            last_hit_at = third
        else:
            last_hit_at = first

        for t in times:
            while t and t[0] <= last_hit_at:
                t.popleft()

        times = tuple(t for t in times if t)

    return n_hits


def tests():
    assert 6 == max_credit(
        (1,2,3,4,5,6),
        (1,2,3,4,5,6,7),
        (1,2,3,4,5,6),
        (0,1,2),
        (1,2,3,4,5,6,7,8)
    )
    print 'one'
    assert 3 == max_credit(
        (100,200,300,1200,6000),
        (),
        (900,902,1200,4000,5000,6001),
        (0,2000,6002),
        (1,2,3,4,5,6,7,8)
    )
    print 'two'
    assert 1 == max_credit(
        (5000,6500),
        (6000,),
        (6500,),
        (6000,),
        (0,5800,6000)
    )
    print 'three'
    print 'tests pass!'


if __name__ == '__main__':
    tests()
