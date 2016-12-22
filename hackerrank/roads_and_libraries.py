"""
https://www.hackerrank.com/contests/world-codesprint-8/challenges/torque-and-development
"""


from collections import deque, defaultdict


def connected_component_sizes(N, graph):
    def _bfs(node):
        n_visited = 0
        q = deque([node])
        
        while q:
            n = q.popleft()
            
            if not visited[n]:
                n_visited += 1
                visited[n] = True
                
                for n2 in graph.get(n, ()):
                    if not visited[n2]:
                        q.append(n2)
                        
        return n_visited
    
    visited = [False for _ in range(N)]
    
    for node in xrange(N):
        if not visited[node]:
            yield _bfs(node)


def min_cost(N, component_sizes, cl, cr):
    if cl <= cr:
        # Cheapest to give every city its own library.
        return N * cl
    
    # Cheapest to give each connected component its own library and
    # reconnect reach component with a minimum spanning tree of roads.
    # Minimum spanning tree is any spanning tree in unweighted graph.
    return sum(cl + cr * (s - 1) for s in component_sizes)


Q = int(raw_input().strip())

for _ in xrange(Q):
    N, M, cl, cr = map(int, raw_input().strip().split())
    graph = defaultdict(list)
    
    for _ in xrange(M):
        u, v = map(lambda x: int(x) - 1, raw_input().strip().split())
        graph[u].append(v)
        graph[v].append(u)
        
    print min_cost(N, connected_component_sizes(N, graph), cl, cr)



#######
# Alternative. Fails on some tests.

def distinct_sets(sets):
    seen = set()
    
    for s in sets:
        if id(s) not in seen:
            yield s
            seen.add(id(s))


Q = int(raw_input().strip())

for _ in xrange(Q):
    N, M, cl, cr = map(int, raw_input().strip().split())
    
    if cl <= cr:
        for _ in xrange(M): raw_input()
        print N * cl
    else:
        nodes = {}
        sets = {}
        new_set_id = 1
        
        for _ in xrange(M):
            u, v = map(int, raw_input().strip().split())
            
            if u in nodes and v in nodes:
                set_id_u, set_id_v = nodes[u], nodes[v]
                setU, setV = sets[set_id_u], sets[set_id_v]
                smaller, larger = (setV, setU) if len(setU) >= len(setV) else (setU, setV)
                larger.update(smaller)
                sets[set_id_u] = larger
                sets[set_id_v] = larger
            elif u in nodes:
                set_id = nodes[u]
                sets[set_id].add(v)
                nodes[v] = set_id
            elif v in nodes:
                set_id = nodes[v]
                sets[set_id].add(u)
                nodes[u] = set_id
            else:
                sets[new_set_id] = set([u, v])
                nodes[u] = new_set_id
                nodes[v] = new_set_id
                new_set_id += 1

        n_singletons = sum(i not in nodes for i in xrange(1, N+1))
        print cl * n_singletons +  sum(cl + cr * (len(connected_component) - 1)
                                       for connected_component in distinct_sets(sets.itervalues()))
