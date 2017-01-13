"""
https://code.google.com/codejam/contest/635101/dashboard#s=p1

This is an example of a GREEDY ALGORITHM. The input data is transformed
into end_locations and operated on in one simple pass. Although this is
a greedy algorithm, the problem statement isn't (or doesn't seem to be)
amenable to reduction to a matroid (as opposed to Kruskal's MST solution).

Note that while we had success "simulating" the process described in the
file-fixit problem (see file_fixit.py), it's unclear what we'd do to simulate
the process described in this problem, and a simulation would likely result in a
more complicated solution, compared to this simple greedy solution.
"""


def solve(N, K, B, T, initial_locations, natural_speeds):
    end_locations = [(x + v * T) for x,v in zip(initial_locations, natural_speeds)]
    # end_locations: sorted by starting locations but values are ending locations.
    k, swaps, cannot_reach_barn = 0, 0, 0

    for loc in reversed(end_locations):
        if k == K:
            break
        elif loc < B:
            cannot_reach_barn += 1
        else:
            swaps += cannot_reach_barn
            k += 1

    return swaps if k >= K else -1


def main():
    C = int(raw_input().strip())

    for c in xrange(1, C+1):
        N, K, B, T = map(int, raw_input().strip().split())
        initial_locations = map(int, raw_input().strip().split())  # Distinct and in increasing order.
        natural_speeds = map(int, raw_input().strip().split())
        n_swaps = solve(N, K, B, T, initial_locations, natural_speeds)
        print 'Case #{}: {}'.format(c, n_swaps if n_swaps >= 0 else 'IMPOSSIBLE')


if __name__ == '__main__':
    main()
