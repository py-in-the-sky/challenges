"""
ABBADiv1

https://arena.topcoder.com/#/u/practiceCode/16526/48829/13922/1/326682

A graph is implied where there are two different types of edges: one representing
appending an 'A' to the string and one representing appending a 'B' followed by
reversing the string.  We'll call these "a-edges" and "b-edges."

The problem gives you two strings, `initial` and `target`.  Implied is a path
along this graph from `initial` to `target`.

The job of this algorithm is to play this path backwards and at every step, check
to ensure that this path is indeed valid.
"""


def a_edge_reversed(s, initial, initial_reversed):
    """
    If an a-edge can be validly reversed, return the result of the reversal.
    Otherwise, return None.
    """
    # precondition for validity:
    if s.endswith('A'):
        s2 = s[:-1]
        # postcondition for validity:
        if initial in s2 or initial_reversed in s2:
            return s2


def b_edge_reversed(s, initial, initial_reversed):
    """
    If a b-edge can be validly reversed, return the result of the reversal.
    Otherwise, return None.
    """
    # precondition for validity:
    if s.startswith('B') and (s.endswith('B') or s.endswith(initial) or s.endswith(initial_reversed)):
        s2 = s[-1:0:-1]
        # postcondition for validity:
        if initial in s2 or initial_reversed in s2:
            return s2


def can_obtain(initial, target):
    initial_reversed = initial[::-1]

    _a_edge_reversed = lambda s: a_edge_reversed(s, initial, initial_reversed)
    _b_edge_reversed = lambda s: b_edge_reversed(s, initial, initial_reversed)

    def _loop(target):
        # loop invariant: len(initial) <= len(target)
        if len(initial) == len(target):
            return initial == target

        t_a = _a_edge_reversed(target)
        t_b = _b_edge_reversed(target)
        return (t_a is not None and _loop(t_a)) or (t_b is not None and _loop(t_b))

    return _loop(target)


class ABBADiv1:
    def canObtain(self, initial, target):
        return "Possible" if can_obtain(initial, target) else "Impossible"



########## Memoized DFS from `initial` to `target` ##########


def memo(f):
    """memoization decorator, taken from Peter Norvig's Design of Computer
    Programs course on Udacity.com"""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = cache[args] = f(*args)
            return result
        except TypeError:  # unhashable argument
            return f(*args)
    return _f


def option_a(s): return s + 'A'
def option_b(s): return (s + 'B')[::-1]


@memo
def can_obtain_memoized_dfs(initial, target):
    # loop invariant: len(initial) <= len(target)
    if len(initial) == len(target):
        return initial == target

    return (can_obtain_memoized_dfs(option_a(initial), target) or
            can_obtain_memoized_dfs(option_b(initial), target))


def tests():
    initial = 'ABBA'
    target = 'ABBAA'
    assert can_obtain(initial, target)
    assert can_obtain_memoized_dfs(initial, target)

    initial = 'ABBA'
    target = 'BABBA'
    assert can_obtain(initial, target)
    assert can_obtain_memoized_dfs(initial, target)

    initial = 'B'
    target = 'ABBA'
    assert not can_obtain(initial, target)
    assert not can_obtain_memoized_dfs(initial, target)

    initial = 'ABABA'
    target = 'BBB' + initial + 'BB'
    assert can_obtain(initial, target)
    assert can_obtain_memoized_dfs(initial, target)

    target = 'A' + target
    assert not can_obtain(initial, target)
    assert not can_obtain_memoized_dfs(initial, target)

    target = 'BBB' + initial + 'BBBB'
    assert not can_obtain(initial, target)
    assert not can_obtain_memoized_dfs(initial, target)

    initial = "A"
    target = "BABA"
    assert can_obtain(initial, target)
    assert can_obtain_memoized_dfs(initial, target)

    initial = "BAAAAABAA"
    target = "BAABAAAAAB"
    assert can_obtain(initial, target)
    assert can_obtain_memoized_dfs(initial, target)

    initial = "A"
    target = "ABBA"
    assert not can_obtain(initial, target)
    assert not can_obtain_memoized_dfs(initial, target)

    # `can_obtain_memoized_dfs` is too slow for bigger inputs

    initial = "AAABBAABB"
    target = "BAABAAABAABAABBBAAAAAABBAABBBBBBBABB"
    assert can_obtain(initial, target)
    # assert can_obtain_memoized_dfs(initial, target)

    initial = "AAABAAABB"
    target = "BAABAAABAABAABBBAAAAAABBAABBBBBBBABB"
    assert not can_obtain(initial, target)
    # assert not can_obtain_memoized_dfs(initial, target)

    print 'tests pass!'


if __name__ == '__main__':
    tests()
