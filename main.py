from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    ### TODO
    def ssp_helper(visited, frontier):
        if len(frontier) == 0:
          return visited
        else:
          stats, node = heappop(frontier)
          distance, edges = stats
          if node in visited:
            return ssp_helper(visited, frontier)
          else:
            visited[node] = (distance, edges)
            for neighbor, weight in graph[node]:
              heappush(frontier, ((distance + weight, edges + 1), neighbor))                
            return ssp_helper(visited, frontier)
        
    frontier = []
    heappush(frontier, ((0, 0), source))
    visited = dict()
    return ssp_helper(visited, frontier)
    
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    ###TODO
    parents = dict()
    visited = set()
    frontier = set([source])

    while len(frontier) != 0:
        parent = frontier.pop()
        neighbors = graph[parent]
        for v in neighbors:
          if v not in parents.keys():
            parents[v] = parent
          frontier.update(graph[v])
          frontier.difference_update(visited)
        visited.add(parent)
    return parents

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    ###TODO
    path = deque()
    current = destination
    while current != parents[current]:
        current = parents[current]
        path.appendleft(current)
    path_str = ""
    for i in path:
        path_str += i
    return path_str

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'
