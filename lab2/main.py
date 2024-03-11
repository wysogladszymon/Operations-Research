from graph import Graph
from djikstra import djikstra

def path_to_graph(path) -> Graph:
    graph = {}
    for node, (previous, distance) in path.items():
        if previous is not None:
            if previous not in graph:
              graph[previous] = []
            graph[previous].append((node, distance))
            if node not in graph:
              graph[node] = []
            graph[node].append((previous, distance))
    return Graph(graph)


def main():  
  g = Graph({
    0: [(1, 10), (2, 15)],
    1: [(0, 10), (2, 4), (3, 2)],
    2: [(0, 15), (1, 5), (4, 12)],
    3: [(1, 2), (4, 8), (5, 16)],
    4: [(2, 12), (3, 8), (6, 6)],
    5: [(3, 16), (6, 7), (7, 9)],
    6: [(4, 6), (5, 7), (8, 3)],
    7: [(5, 9), (8, 11), (9, 13)],
    8: [(6, 3), (7, 11), (9, 1)],
    9: [(7, 13), (8, 1)]
})
  path = djikstra(g)
  # print(path)
  tree = path_to_graph(path)
  print(tree)
  

if __name__ == '__main__':
  main()
