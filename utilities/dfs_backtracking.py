"""
Instead of relying on a stack (implicitly with recursion, or explicitly)
to perform DFS, use backtracking, facilitated by "parent" pointers.
Following "parent" pointers takes you backwards along the path between
current node and source node.

Idea of using `parent` mapping for backtracking taken from www.mooc.labinthewild.org
"""


def dfs_backtracking(node, adjacencies, visited):
    parent = {node: None}
    _visited = lambda node: node in visited or node in parent

    while node is not None:
        print 'node:', node
        next_node = next((n for n in adjacencies[node] if not _visited(n)), None)

        if next_node:
            print 'next node:', next_node
            parent[next_node] = node
            node = next_node
        else:
            node = parent[node]

    return parent
