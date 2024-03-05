from graph import  Graph

def conversion(visited):
  v = {node : index for index, node in enumerate(visited)}
  return {k: v[k] for k in sorted(v.keys())} 

def main():
  G1 = Graph({
    0: [1, 2, 3, 4],
    1: [2, 3, 4, 5],
    2: [3, 4, 5, 6],
    3: [4, 5, 6, 7],
    4: [5, 6, 7, 8],
    5: [6, 7, 8, 9],
    6: [7, 8, 9, 0],
    7: [8, 9, 0, 1],
    8: [9, 0, 1, 2],
    9: [0, 1, 2, 3]
})

  G2 = Graph({
    0: [1, 2],
    1: [0, 2, 3],
    2: [0, 1, 3],
    3: [1, 2, 4],
    4: [3, 5],
    5: [4, 6],
    6: [5, 7],
    7: [6, 8],
    8: [7],
    9: []
})
  G3  = Graph({
    0: [1],
    1: [2],
    2: [3],
    3: [4],
    4: [5],
    5: [6],
    6: [7],
    7: [8],
    8: [9],
    9: []
    })
  
  names = ['Graf spójny cykliczny', 'Graf niespójny cykliczny', 'Graf spójny acykliczny']
  graphs = [G1, G2, G3]

  for name, graph in zip(names, graphs):
    print(name)
    print('Graf:', graph)
    print('DFS:', conversion(graph.dfs(3)))
    print('Cykliczny:', 'Tak' if graph.iscyclic() else 'Nie')
    print('Spójny:', 'Tak' if graph.isconnected() else 'Nie')
    print('\n ')
    
if __name__ == '__main__':
  main()
