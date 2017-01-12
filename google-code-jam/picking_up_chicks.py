"""
https://code.google.com/codejam/contest/635101/dashboard#s=p1
"""


def merge_sort_count_inversions(A):
    if len(A) <= 1:
        return 0, A

    b_inversions, B = merge_sort_count_inversions(A[:len(A) / 2])
    c_inversions, C = merge_sort_count_inversions(A[len(A) / 2:])
    inversions = b_inversions + c_inversions
    b, c = 0, 0
    A = []

    while b < len(B) and c < len(C):
        if B[b] <= C[c]:
            A.append(B[b])
            b += 1
        else:
            A.append(C[c])
            c += 1
            # Starting positions of B are less than those of C, so count
            # inversions here.
            inversions += (len(B) - b)

    d, D = (b, B) if b < len(B) else (c, C)
    A += D[d:]
    return inversions, A



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
