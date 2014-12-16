"""
see: https://www.hackerrank.com/contests/quora-haqathon/challenges/archery

Due to the simplifications in the problem statement, an arrow will instersect
with a circle either once or twice.

R is a collection of radius lengths.  For each arrow, iterate through each r
in R: see if the arrow has 0, 1, or 2 points of length r from the origin.

Optimizations:
    - if both endpoints of the arrow are further than r from the origin, then
      the arrow instersects circle r 0 or 2 times (no Q formed)
    - if both are less than r from the origin, then the arrow instersects 0
      circle r 0 times (no Q formed)
    - if one endpoint is further than r form origin and the other is less, then
      a Q is formed
"""

from math import pow, sqrt
from bisect import bisect

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

@memo
def euclidean_distance(x, y):
    return sqrt(pow(x, 2) + pow(y, 2))

def count_qs(arrow, radii):
    x1, y1, x2, y2 = arrow
    d1, d2 = sorted([euclidean_distance(x1, y1), euclidean_distance(x2, y2)])
    m, n = bisect(radii, d1), bisect(radii, d2)
    return n - m

def parse_arrow(arrow_text):
    return map(int, arrow_text.split())

N = int(raw_input())
radii = sorted(map(int, raw_input().split()))
M = int(raw_input())
arrows = (parse_arrow(raw_input()) for _ in xrange(M))

print sum(count_qs(a, radii) for a in arrows)
