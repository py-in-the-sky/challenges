"""
http://www.geeksforgeeks.org/print-k-sum-paths-binary-tree/
"""


from collections import defaultdict


def print_k_sum_paths_binary_tree(root_node, k):

    def _preorder_traversal(node, sum_total):
        if node is None:
            return

        sum_total2 = sum_total + node.value
        index = len(node_values)
        sum_indices[sum_total2].add(index)
        node_values.append(node.value)

        for i in sum_indices[sum_total2 - k]:
            print ' '.join(str(node_values[j]) for j in xrange(i+1, len(node_values)))

        _preorder_traversal(node.left, sum_total2)
        _preorder_traversal(node.right, sum_total2)

        sum_indices[sum_total2].remove(index)
        node_values.pop()

    # sum_indices is a dictionary. sum_indices[x] is a set of indices, i,
    # into node_values such that sum(node_values[:i+1]) the path is x.
    sum_indices = defaultdict(set)
    sum_indices[0].add(0)
    node_values = [0]
    _preorder_traversal(root_node, 0)


class Node:
    left = None
    right = None
    value = None

    def __init__(self, value):
        self.value = value


def main():
    k = 5
    root_node = Node(1)
    n1 = Node(3)
    n2 = Node(-1)
    n3 = Node(2)
    n4 = Node(1)
    n5 = Node(4)
    n6 = Node(5)
    n7 = Node(1)
    n8 = Node(1)
    n9 = Node(2)
    n10 = Node(6)

    root_node.left, root_node.right = n1, n2
    n1.left, n1.right = n3, n4
    n2.left, n2.right = n5, n6
    n4.left = n7
    n5.left, n5.right = n8, n9
    n6.right = n10

    print_k_sum_paths_binary_tree(root_node, k)


if __name__ == '__main__':
    main()
