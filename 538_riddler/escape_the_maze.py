"""
https://fivethirtyeight.com/features/come-on-down-and-escape-the-maze/

Graph Key:
  * => star
  x => skull and crossbones
  u => up arrow
  d => down arrow
  l => left arrow
  r => right arrow
  v => up-down arrow
  h => left-right arrow
"""


from collections import namedtuple
import heapq


MAZE = """vu20rrrxv3h1h00xuv3v
rhdurl2vx01v2u13vdrv
hv2vh3ldvvldhlvv2vxr
vhhhhlhr0v3v3vh1hhl1
huhdxvhh1xv0l0r13llh
1vvhv1vhhv3hdhlhvrhh
vdvhvxvhh1v2hhvvhhr1
32hhhvh3rv3v3uuhvvdu
r0ur12rvhv33v0lxhhvd
vhdrl2vdh0v1hvulh0vv
vh2v1dvuu0*2h3vvhuhh
hdxh3lvvvhvl2vhvhvuv
vxulhvvuvvlh10h3ldhv
2xrdvvvvx1vvh0vr03hh
xv2rrdh1uv0h31lhxhhv
lddh1hvvdhhvv10uvvv0
hd3hvh2dhuhl0x2h1hhv
x02hhvvd2002hurhhhvv
hh1hvv3vh3vv20uuh2rh
lhhh3vvvrhlh12h2hdvu""".splitlines()


SearchState = namedtuple("SearchState", "score coordinates")


def solve(square_maze):
  priority_queue = PriorityQueue(perimeter_starting_states(square_maze))
  visited_coordinates = set()

  while len(priority_queue) > 0:
    search_state = priority_queue.pop()

    if get_char(search_state.coordinates, square_maze) == "*":
      return search_state

    visited_coordinates.add(search_state.coordinates)
    for coords in neighbors(search_state.coordinates, square_maze):
      if coords not in visited_coordinates:
        score = search_state.score + get_score(coords, square_maze)
        priority_queue.push(SearchState(score, coords))


def perimeter_starting_states(square_maze):
  side_length = len(square_maze)
  top_border = set((0, i) for i in xrange(side_length))
  bottom_border = set((side_length-1, i) for i in xrange(side_length))
  left_border = set((i, 0) for i in xrange(side_length))
  right_border = set((i, side_length-1) for i in xrange(side_length))
  perimeter = top_border | bottom_border | left_border | right_border
  return (SearchState(get_score(coordinates, square_maze), coordinates)
          for coordinates in perimeter)


def get_char(coordinates, square_maze):
  row, col = coordinates
  return square_maze[row][col]


def get_score(coordinates, square_maze):
  char = get_char(coordinates, square_maze)
  try:
    return "0123456789".index(get_char(coordinates, square_maze))
  except ValueError: # Not a digit.
    return 0


def neighbors(coordinates, square_maze):
  up, down, left, right = (-1, 0), (1, 0), (0, -1), (0, 1)
  moves = {
    "*": [],
    "x": [],
    "v": [up, down],
    "h": [left, right],
    "u": [up],
    "d": [down],
    "l": [left],
    "r": [right],
  }
  moves_for_int = [up, down, left, right]
  char = get_char(coordinates, square_maze)
  row, col = coordinates
  neighbors = [(row + row_delta, col + col_delta)
               for row_delta,col_delta in moves.get(char, moves_for_int)]
  return [(r,c) for r,c in neighbors
          if 0 <= r < len(square_maze) and 0 <= c < len(square_maze)]


class PriorityQueue:
  def __init__(self, elements):
    self.heap = list(elements)
    heapq.heapify(self.heap)

  def __len__(self):
    return len(self.heap)

  def pop(self):
    return heapq.heappop(self.heap)

  def push(self, element):
    heapq.heappush(self.heap, element)


if __name__ == '__main__':
  print solve(MAZE).score
