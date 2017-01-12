"""
Determine whether a given directed graph is a directed acyclic graph (DAG).
"""


def is_dag(nodes, adjacencies):
    # import sys; sys.setrecursionlimit(2000)  # if you need a greater recursion depth
    gray = set()
    black = set()

    def _dfs_detect_cycle_from(node):
        if node in black:
            return False
        elif node in gray:
            # DFS is downstream from and has cycled back to node
            return True

        gray.add(node)  # Mark beginning of DFS from node
        result = any(_dfs_detect_cycle_from(n) for n in adjacencies[node])
        black.add(node)  # Mark exhaustive DFS from node complete
        return result

    return not any(_dfs_detect_cycle_from(node) for node in nodes)


def is_dag_backtracking(nodes, adjacencies):
    gray = {}
    black = set()

    def _dfs_detect_cycle_from(node):
        if node in black:
            return False

        gray = {node: None}

        while node is not None:
            next_node = next((n for n in adjacencies[node] if n not in black), None)

            if next_node in gray:
                # Cycle detected
                return True
            elif next_node is not None:
                # Mark next node as gray and begin DFS from it
                gray[next_node] = node  # Mark beginning of DFS from node
                node = next_node
            else:
                # No next node to search from; mark as exhaustively searched and then backtrack
                black.add(node)  # Mark exhaustive DFS from node complete
                node = gray[node]

        return False

    return not any(_dfs_detect_cycle_from(node) for node in nodes)


def is_dag_explicit_stack(adjacencies, n_nodes):
    "Explicitly manage stack, rather than rely on recursion."
    WHITE, GREY, BLACK = 0, 1, 2
    visited = [WHITE for _ in xrange(n_nodes)]
    # WHITE means you've never been popped off the stack before.
    # GREY means we're doing DFS from you right now.
    # BLACK means we've completed exhaustive DFS from you.

    # Therefore, it we run into a GREY node while adding nodes to
    # the stack in our DFS, that means there's a cycle.

    def _leads_to_cycle(node):
        if visited[node] is BLACK:
            return False

        stack = [node]

        while stack:
            node = stack.pop()
            color = visited[node]
            if color is GREY:
                visited[node] = BLACK
            elif color is WHITE:
                visited[node] = GREY
                stack.append(node)
                for node2 in adjacencies.get(node, ()):
                    color2 = visited[node2]
                    if color2 is GREY:
                        return True
                    elif color2 is WHITE:
                        stack.append(node2)

        return False

    # Iterate over all nodes; use DFS as a subroutine to determine whether
    # a cycle exists downstream from a node.
    return not any(_leads_to_cycle(node) for node in adjacencies)
