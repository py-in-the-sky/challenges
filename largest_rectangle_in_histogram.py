"""
https://www.youtube.com/watch?v=VNbkzsnllsU
"""


def largest_rectangle_in_histogram(histogram):
    "Return area of largest rectangle under histogram."
    assert all(height >= 0 for height in histogram)

    # Use stacks to keep track of how long a rectangle of height h
    # extends to the right.

    largest = 0
    positions = [0]
    heights = [0]

    for i,height in enumerate(histogram):
        if height > heights[-1]:
            # Track new tallest rectangle.
            positions.append(i)
            heights.append(height)
        elif height < heights[-1]:
            # Close rectangles taller than height.
            while height < heights[-1]:
                h, p = heights.pop(), positions.pop()
                largest = max(largest, h * (i - p))

    i = len(histogram)
    while heights:
        # Close open rectangles.
        h, p = heights.pop(), positions.pop()
        largest = max(largest, h * (i - p))

    return largest


def tests():
    assert largest_rectangle_in_histogram([]) == 0
    assert largest_rectangle_in_histogram([4]) == 4
    assert largest_rectangle_in_histogram([1, 3, 2, 1, 2]) == 5
    assert largest_rectangle_in_histogram(map(lambda x: x * 10000000, [1, 3, 2, 1, 2])) == 5 * 10000000
    assert largest_rectangle_in_histogram([1, 2, 1, 3, 2, 0, 1]) == 5

    print 'tests pass!'
