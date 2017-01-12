"""
https://code.google.com/codejam/contest/1985486/dashboard#s=p3
"""


from collections import defaultdict


def solve(dependencies, required_technologies):
    """
    Topological sorting.

    Starting from each required technology, each dependency will be visited --
    and only each dependency will be visited. Therefore, in the end,
    `order` will be exactly the technologies that need to be developed to
    satisfy `required_technologies`.

    By using the post-order traversal to append to `order`, we build a
    topological sorting of all the technologies required.

    `dependencies` forms a (potentially disconnected) DAG. `visited` is a
    subset of nodes from the DAG. `order` is a topological sorting of the nodes
    in `visited`.
    """
    def _dfs(tech):
        if tech not in visited:

            for dep in dependencies[tech]:
                _dfs(dep)

            visited.add(tech)
            order.append(tech)

    visited = set()
    order = []

    for tech in required_technologies:
        _dfs(tech)

    return order


def main():
    T = int(raw_input().strip())

    for t in xrange(1, T+1):
        M = int(raw_input().strip())
        deps = defaultdict(list)

        for a,b in (raw_input().strip().split(':') for _ in xrange(M)):
            deps[a].append(b)

        Q = int(raw_input().strip())
        qs = tuple(raw_input().strip() for _ in xrange(Q))

        order = solve(deps, qs)

        print 'Case #{}: {}'.format(t, len(order))
        for tech in order:
            print tech


if __name__ == '__main__':
    main()
