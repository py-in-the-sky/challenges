"""
https://www.interviewcake.com/question/python/find-rotation-point

In discussions below, let rp be the index of the rotation point.

Assumptions on input words:

    * words is sorted and then rotated
    * hence, words are in sorted order from 0 to rp-1 and from rp to the end
    * words[i] < words[rp] for i < rp
    * words [j] < words[rp] for j >= rp

Loop invariants of rotation_point:

    * hi == len(words) or words[rp] <= words[hi] <= words[-1]
    * lo == -1 or words[0] <= words[lo] < words[rp]
    * therefore, lo < rp <= hi throughout

Argument for why the algorithm ends: if (hi - lo > 1), then
(lo < mid < hi) where (mid = (hi + lo) // 2). Therefore, (hi - lo)
shrinks on every iteration.

Note that when the algorithm ends, it must be the case that
(hi - lo == 1). Proof by contradiction: let hi and lo be the
values of the indices at the end of the algorithm, and let
hi' and lo' be the values at the start of the last iteration.
Now assume that when the algorithm ends, we have (hi - lo < 1).
In the last iteration of the loop, the value mid was assigned to
either hi or lo. If hi, then hi == mid == ((hi' + lo') // 2)
== ((hi' + lo) // 2) <= lo, which implies hi' <= lo == lo', which
contradicts our loop invariants. If lo, then lo == mid == ((hi' + lo') // 2)
== ((hi + lo') // 2) >= hi, which implies lo' >= hi == hi', which
contradicts our loop invariants.

Argument for the correctness of the algorithm: it follows from the
loop invariants that at the end, (words[hi] >= words[rp]) and
(words[lo] < words[rp]). Combine this with the ending condition of
(hi - lo == 1), then we have words[lo] == words[hi-1] < words[rp],
and therefore words[hi] == words[rp].

In other words, when the algorithm ends, words[hi] is the smallest
element in words.

Edge cases:

    * Could we ever end with hi == len(words)? No. Except for the
      empty list, rp always exists in words since the values of
      words are distinct and there's therefore necessarily a
      smallest element. At the end, lo == hi-1 < rp < len(words),
      and therefore hi == rp < len(words).
    * What if rp == 0? Then words[mid] <= words[-1] for all possible
      values of mid, and therefore in the end we must have hi == 0.
"""


def rotation_point(words):
    lo, hi = -1, len(words)

    while hi - lo > 1:
        mid = (hi + lo) // 2

        if words[mid] <= words[-1]:
            hi = mid
        else:
            lo = mid

    return hi


def tests():
    words = [
        'ptolemaic',
        'retrograde',
        'supplant',
        'undulate',
        'xenoepist',
        'asymptote',  # <-- rotates here!
        'babka',
        'banoffee',
        'engender',
        'karpatka',
        'othellolagkage',
    ]
    assert rotation_point(words) == 5

    words = [
        'banoffee',
        'engender',
        'karpatka',
        'othellolagkage',
        'ptolemaic',
        'retrograde',
        'supplant',
        'undulate',
        'xenoepist',
        'asymptote',  # <-- rotates here!
        'babka',
    ]
    assert rotation_point(words) == 9

    words = [
        'babka',
        'banoffee',
        'engender',
        'karpatka',
        'othellolagkage',
        'ptolemaic',
        'retrograde',
        'supplant',
        'undulate',
        'xenoepist',
        'asymptote',  # <-- rotates here!
    ]
    assert rotation_point(words) == 10

    words = [
        'asymptote',  # <-- rotates here!
        'babka',
        'banoffee',
        'engender',
        'karpatka',
        'othellolagkage',
        'ptolemaic',
        'retrograde',
        'supplant',
        'undulate',
        'xenoepist',
    ]
    assert rotation_point(words) == 0

    words = [
        'undulate',
        'xenoepist',
        'asymptote',  # <-- rotates here!
        'babka',
        'banoffee',
        'engender',
        'karpatka',
        'othellolagkage',
        'ptolemaic',
        'retrograde',
        'supplant',
    ]
    assert rotation_point(words) == 2

    assert rotation_point(['a']) == 0

    assert rotation_point([]) == 0

    print 'Tests pass!'
