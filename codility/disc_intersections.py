"""
Disc Intersections

https://codility.com/demo/take-sample-test/ndi/

A is an array representing N = len(A) circles (discs) on a plane.  For an
arbitrary index j, A[j] is the circle's radius and (j, 0) is its center's
(x, y) coordinate.

Runtime: O(NlogN)
Extra Space: O(N)

This is fundamentally a counting problem.  It's easy to count all leftmost points
that are LTE a disc's rightmost point, and it's easy to count all discs to the
left of a disc.  Therefore, we count the intersections between a disc and all
discs to its right with the following:

    bisect_right(leftmost_points, rightmost_point) - (j + 1)
"""


from bisect import bisect_right


def solution(A):
    leftmost_points = sorted(j-r for j,r in enumerate(A))
    intersections = 0

    for j,r in enumerate(A):
        rightmost_point = j + r
        rightside_intersections = bisect_right(leftmost_points, rightmost_point) - (j + 1)
        intersections += rightside_intersections

    return intersections if intersections <= 10000000 else -1
