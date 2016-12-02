from collections import defaultdict


def bits(n):
    "Generator. All bits, from least to most significant."
    while n > 0:
        yield n & 1
        n >>= 1


def n_bits(n):
    "Number of nodes in the set."
    return sum(bits(n))


def node_sets(n):
    "All node sets that include node 0, sorted by set size."
    bit_sets = set(n for n in range(2, 2**n) if (n & 1) == 1)
    return sorted(bit_sets, key=n_bits)


def active_bits(n):
    "Generator. All nodes in the set."
    return (i for i,bit in enumerate(bits(n)) if bit == 1)


def hamiltonian_cycle(graph, N):
    """
    Predicate. True if the graph consitutes a Hamiltonian cycle -- that is, if
    you can start at a node, visit all nodes in the graph, and end at the start
    node, such that all nodes are visited once (the start node will be visited
    twice).

    All N nodes must be represented by the integers [0, N).

    Since any node can be the start node, we use 0 as the start node.

    This algorithm uses dynamic programming, starting with the node set containing
    just the start node and then building out from there to larger node sets that
    are connected to the start node and that form a Hamiltonian path.
    """
    if N <= 1:
        return True

    hamiltonian_paths = defaultdict(dict)
    hamiltonian_paths[1 << 0][0] = (0,)

    for s in node_sets(N):
        for n in (n for n in active_bits(s) if n != 0):
            s2 = s ^ (1 << n)
            # Dynamic programming step: remove all nodes, one at a time, except
            # for the start node, from the proposed set. If the smaller set
            # forms a Hamiltonian path and has an edge to the removed node, then
            # the proposed set also forms a Hamiltonian path.
            for end_point,path in hamiltonian_paths[s2].items():
                if end_point in graph and n in graph[end_point]:
                    hamiltonian_paths[s][n] = path + (n,)

    # 2**N - 1 is the node set that contains all nodes of the graph.
    # Each Hamiltonian path in hamiltonian_paths[2**N - 1] whose endpoint
    # has an edge to 0 forms a Hamiltonian cycle.
    cycles = (path + (0,)
              for path in hamiltonian_paths[2**N - 1].values()
              if 0 in graph[path[-1]])

    return tuple(cycles)


def tests():
    graph = {
        0: {1, 2},
        1: {0, 3},
        2: {3},
        3: {4},
        4: {1, 2, 3}
    }

    cycles = hamiltonian_cycle(graph, 5)
    assert cycles
    assert (0, 2, 3, 4, 1, 0) in cycles

    graph = {
        0: {1},
        1: {0, 2},
        2: {1}
    }

    assert not hamiltonian_cycle(graph, 3)

    graph = {
        0: {1},
        1: {2, 3},
        2: {0},
    }

    assert not hamiltonian_cycle(graph, 4)

    print('tests pass!')


if __name__ == '__main__':
    tests()
