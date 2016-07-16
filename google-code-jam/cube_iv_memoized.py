"""
https://code.google.com/codejam/contest/6214486/dashboard

Max recursion depth exceeded on large input.  This could be
avoided by visiting rooms in order of their assigned value,
largest value first.
"""


import itertools as it


FOUR_DOORS = ((1, 0), (-1, 0), (0, 1), (0, -1))


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


def neighbors(maze, index):  # runtime: O(1)
    i, j = index
    S = len(maze)
    neighbor_coords = ((i+a, j+b) for a,b in FOUR_DOORS)
    return ((a,b,maze[a][b]) for a,b in neighbor_coords if 0<=a<S and 0<=b<S)


@memo
def travel_distance(maze, room_index):
    i, j = room_index
    room_value = maze[i][j]
    next_room_index = next(((i2,j2)
                            for i2,j2,v in neighbors(maze, room_index)
                            if v == room_value+1), None)

    if next_room_index is None:
        return 1

    return 1 + travel_distance(maze, next_room_index)


def find_winner(maze):
    S = len(maze)
    maze_indices = it.product(xrange(S), xrange(S))
    room_value = lambda i, j: maze[i][j]
    winner_room_index = max(maze_indices,
                            key=lambda ii: (travel_distance(maze, ii), -room_value(*ii)))
    return room_value(*winner_room_index), travel_distance(maze, winner_room_index)


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
