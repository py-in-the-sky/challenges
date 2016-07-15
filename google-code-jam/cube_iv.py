"""
https://code.google.com/codejam/contest/6214486/dashboard
"""


import itertools as it


FOUR_DOORS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbors(maze, i, j):  # runtime: O(1)
    S = len(maze)
    neighbor_coords = ((i+a, j+b) for a,b in FOUR_DOORS)
    return (maze[a][b] for a,b in neighbor_coords if 0<=a<S and 0<=b<S)


def indicate_plus_1_neighbor(maze):  # runtime: O(S**2)
    S = len(maze)
    has_plus_1_neighbor = [None for _ in xrange(S**2 + 1)]  # runtime: O(S**2)

    for i,j in it.product(xrange(S), xrange(S)):  # runtime: O(S**2)
        n = maze[i][j]
        has_plus_1_neighbor[n] = any(neighbor == n+1 for neighbor in neighbors(maze, i, j))

    assert all(e is not None for e in has_plus_1_neighbor[1:])
    return has_plus_1_neighbor


def find_winner(maze):  # runtime: O(S**2)
    """maze is a square 2D array of natural numbers 1..S**2 where S is
    the side length of maze."""
    S = len(maze)
    has_plus_1_neighbor = indicate_plus_1_neighbor(maze)  # runtime: O(S**2)
    travel_distances = [1 for _ in xrange(S**2 + 1)]  # runtime: O(S**2)

    for n in xrange(S**2, 0, -1):  # runtime: O(S**2)
        if has_plus_1_neighbor[n]:
            travel_distances[n] = 1 + travel_distances[n+1]

    room_no = max(xrange(1, S**2 + 1), key=lambda r: travel_distances[r])  # runtime: O(S**2)
    return room_no, travel_distances[room_no]


def main():
    T = int(raw_input().strip())
    raw_input()

    for t in xrange(1, T+1):
        S = int(raw_input().strip())
        maze = tuple(tuple(map(int, raw_input().split())) for _ in xrange(S))
        r, d = find_winner(maze)
        print "Case #{}: {} {}".format(t, r, d)


if __name__ == '__main__':
    main()
