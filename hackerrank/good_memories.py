"""
https://www.hackerrank.com/contests/booking-passions-hacked-backend/challenges/good-memories/submissions/code/6536390

Problem reduction: do all friends' sequences form a directed acyclic graph (DAG)?

Runtime: O(V + E)
"""


import sys
from collections import defaultdict


sys.setrecursionlimit(2000)  # for recursive depth-first search on up to 1000 attractions


def big_union(sets): return frozenset().union(e for s in sets for e in s)


def is_dag(graph, n_nodes):
    # painting method from http://codeforces.com/blog/entry/4907?#comment-99802
    WHITE, GREY, BLACK = 0, 1, 2
    visited = [WHITE for _ in xrange(n_nodes)]

    def _has_back_edge(node):
        if visited[node] == BLACK:
            return False
        elif visited[node] == GREY:
            return True

        visited[node] = GREY
        next_nodes = graph.get(node)
        has_back_edge = any(_has_back_edge(node2) for node2 in next_nodes) if next_nodes else False
        visited[node] = BLACK
        return has_back_edge

    return not any(_has_back_edge(node) for node in graph)


def create_graph(sequences):
    places = big_union(sequences)
    n_places = len(places)
    place_id_mapping = {p:i for i,p in enumerate(places)}
    graph = defaultdict(set)

    for seq in sequences:
        for a1,a2 in zip(seq, seq[1:]):
            graph[place_id_mapping[a1]].add(place_id_mapping[a2])

    return {k:tuple(v) for k,v in graph.iteritems()}, n_places


def solve(sequences):
    graph, n_nodes = create_graph(sequences)
    return is_dag(graph, n_nodes)


def parse_sequence(line):
    places = (e.strip() for e in line.strip().split(','))
    return tuple(p for p in places if p)


def main():
    x = int(raw_input().strip())
    for _ in xrange(x):
        n = int(raw_input().strip())
        sequences = tuple(parse_sequence(raw_input()) for _ in xrange(n))
        print 'ORDER EXISTS' if solve(sequences) else 'ORDER VIOLATION'


if __name__ == '__main__':
    main()
