from collections import defaultdict


def bellman_ford(graph, node, N):
    """
    Implementation of the Bellman-Ford algorithm, a single-source shortest
    paths algorithm. It calculates the shortest path from the given source node
    to all other nodes in the graph. It's slower than Dijkstra's algorithm, but
    unlike Dijkstra's, it handles edges with a negative weight.

    Returns (d, p, on_negative_cycle) triple:
        * d is a mapping from each node in the graph to its shortest distance
          from the source node.
        * p is a mapping from each node to its predecessor in the search.
        * on_negative_cycle is a subset of all the nodes that have a distance
          from node of negative infinity.

    Runtime: O(|V| * |E|) -- number of nodes times number of edges

    The shortest path from a node to the source node can be derived using p.
    E.g., for a node n0, n1 = p[n0] is its predecessor, and n2 = p[n1] is its
    predecessor. Follow this pattern until the source node is reached, and you
    will have reconstructed the shortest path from source node to n0.

    You can perform DFS from the nodes in `on_negative_cycle` in order to collect
    all nodes that are "downstream" from them. The set of nodes returned from the
    DFS will be the set of all nodes in the graph whose distance from the source
    node is negative infinity.

    Inputs:
        * Graph describes edges via a dictionary:
            {node: [(node1, weight), (node2, weight), ...]}
        * node: the identifier for the source node
            All identifiers should be in the range [0, N)
        * N: the number of nodes in the graph
    """
    d = defaultdict(lambda: float('inf'))
    d[node] = 0
    p = {node: None}

    for _ in range(N-1):
        # N-1 because with N nodes, the furthest away any node could be from
        # the source node is N-1 moves, or N-1 edges.
        # The first iteration will update all nodes that are one edge away
        # from the source; the kth iteration, all nodes k edges away. After
        # N-1 iterations, all nodes in the graph will have been updated.

        for u in graph:
            for v,weight in graph[u]:
                # Iterate over each edge and update distances.
                if d[u] + weight < d[v]:
                    d[v] = d[u] + weight
                    p[v] = u

    on_negative_cycle = set(v
                            for u in graph
                            for v,weight in graph[u]
                            if d[u] + weight < d[v])
    # One last iteration. If any node would still change its distance from the
    # source node, it must not have a shortest path from the source node:
    # it must be on a negative cycle.

    return d, p, on_negative_cycle
